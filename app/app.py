from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

st.set_page_config(page_title='Who Should a College Help First?', layout='wide')

DATA_PATH = Path(__file__).parent.parent / 'data' / 'data.csv'
CUTOFF = 0.35
CATEGORICAL = ['Marital status', 'Application mode', 'Course', 'Previous qualification',
               'Nacionality', "Mother's qualification", "Father's qualification",
               "Mother's occupation", "Father's occupation"]
HELP = {'Both': 'Advisor meeting', 'Money': 'Financial aid office',
        'Grades': 'Tutoring', 'Other': 'Light check-in'}


@st.cache_resource
def load_and_train():
    df = pd.read_csv(DATA_PATH, sep=';')
    df.columns = df.columns.str.strip()
    df['dropout'] = (df['Target'] == 'Dropout').astype(int)

    sem1 = [c for c in df.columns if c.startswith('Curricular units 1st sem')]
    sem2 = [c for c in df.columns if c.startswith('Curricular units 2nd sem')]
    features = [c for c in df.columns if c not in ['Target', 'dropout'] + sem2]

    X_train, X_test, y_train, y_test = train_test_split(
        df[features], df['dropout'], test_size=0.2, stratify=df['dropout'], random_state=42)

    cats = [c for c in features if c in CATEGORICAL]
    nums = [c for c in features if c not in CATEGORICAL]
    model = Pipeline([
        ('prep', ColumnTransformer([
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cats),
            ('num', StandardScaler(), nums)])),
        ('model', LogisticRegression(max_iter=2000, class_weight='balanced')),
    ])
    model.fit(X_train, y_train)

    students = X_test.copy()
    students['risk'] = model.predict_proba(X_test)[:, 1]
    students['dropped_out'] = y_test
    students = students.sort_values('risk', ascending=False)
    students['rank'] = range(1, len(students) + 1)
    students['segment'] = students.apply(segment, axis=1)

    train_mean = model.named_steps['prep'].transform(X_train).mean(axis=0)
    return model, students, train_mean


def segment(row):
    money = row['Tuition fees up to date'] == 0 or row['Debtor'] == 1
    enrolled = row['Curricular units 1st sem (enrolled)']
    passed = row['Curricular units 1st sem (approved)']
    grades = enrolled == 0 or passed / enrolled < 0.5
    if money and grades:
        return 'Both'
    if money:
        return 'Money'
    if grades:
        return 'Grades'
    return 'Other'


def reasons(model, student_row, train_mean):
    """How much each feature pushed this student's risk up (+) or down (-)."""
    prep = model.named_steps['prep']
    coef = model.named_steps['model'].coef_[0]
    x = prep.transform(student_row.to_frame().T)[0]
    contrib = coef * (x - train_mean)
    names = prep.get_feature_names_out()
    original = [n.replace('num__', '') if n.startswith('num__')
                else n.replace('cat__', '').rsplit('_', 1)[0] for n in names]
    return pd.Series(contrib).groupby(original).sum().sort_values()


model, students, train_mean = load_and_train()
feature_cols = list(model.feature_names_in_)

# ---------- Page ----------
st.title('Who Should a College Help First?')
st.write('A dropout risk model that helps an advising office decide who to contact first '
         'and what kind of help to offer. Pick a student to see their risk, their '
         'segment, and the top reasons behind the score.')
st.caption('The model only suggests who to talk to. An advisor makes the final call, '
           'and students are never told they are "high risk."')

with st.sidebar:
    st.header('Pick a student')
    show = st.radio('Show', ['All test students', 'Top 10% outreach list', 'Flagged only'])
    pool = students
    if show == 'Top 10% outreach list':
        pool = students.head(int(round(len(students) * 0.10)))
    elif show == 'Flagged only':
        pool = students[students['risk'] >= CUTOFF]
    choice = st.selectbox(
        'Student (ranked by risk)', pool.index,
        format_func=lambda i: f"Rank {students.loc[i, 'rank']}: risk {students.loc[i, 'risk']:.0%}")
    st.caption(f'{len(pool)} students in this list. Data: 885 test students the model never trained on.')

s = students.loc[choice]
flagged = s['risk'] >= CUTOFF

c1, c2, c3 = st.columns(3)
c1.metric('Risk score', f"{s['risk']:.0%}")
c2.metric('Flagged?', 'Yes' if flagged else 'No', help=f'Flagged when risk is {CUTOFF:.0%} or higher')
c3.metric('Suggested help', HELP[s['segment']] if flagged else 'None needed',
          help='Money: tuition or debt issue. Grades: passed under half of semester 1 courses.')

left, right = st.columns(2)
with left:
    st.subheader('Top reasons')
    r = reasons(model, s[feature_cols], train_mean)
    up = r[r > 0].sort_values(ascending=False).head(3)
    down = r[r < 0].head(3)
    st.markdown('**Raising risk**')
    for name, val in up.items():
        st.write(f'🔺 {name} (+{val:.2f})')
    st.markdown('**Lowering risk**')
    for name, val in down.items():
        st.write(f'🔻 {name} ({val:.2f})')
    st.caption('Each number is how much that feature moved the score compared with an average student.')

with right:
    st.subheader('Student profile')
    profile = {
        'Age at enrollment': int(s['Age at enrollment']),
        'Gender': 'Male' if s['Gender'] == 1 else 'Female',
        'Scholarship': 'Yes' if s['Scholarship holder'] == 1 else 'No',
        'Tuition up to date': 'Yes' if s['Tuition fees up to date'] == 1 else 'No',
        'In debt': 'Yes' if s['Debtor'] == 1 else 'No',
        'Semester 1 courses passed': f"{int(s['Curricular units 1st sem (approved)'])} of "
                                     f"{int(s['Curricular units 1st sem (enrolled)'])}",
        'Semester 1 average grade (0-20)': round(float(s['Curricular units 1st sem (grade)']), 1),
        'Segment': s['segment'],
    }
    st.table(pd.DataFrame({'Value': [str(v) for v in profile.values()]}, index=profile.keys()))

with st.expander('What actually happened? (for checking the model only)'):
    st.write('Dropped out' if s['dropped_out'] == 1 else 'Did not drop out (graduated or still enrolled)')

with st.expander('How this works and its limits'):
    st.markdown(
        '- **Model:** logistic regression using enrollment data plus semester 1 results.\n'
        '- **Cutoff:** 35%, chosen because a missed dropout was weighted 5x a false alarm.\n'
        '- **Top 10%:** 87 of the 88 highest-risk test students really dropped out.\n'
        '- **Fairness:** the model gives more false alarms to students 25+ and men, and misses '
        'more scholarship holders who drop out. Check these gaps every semester.\n'
        '- **Data:** 4,424 students from one university in Portugal (UCI, CC BY 4.0). No race column.')
