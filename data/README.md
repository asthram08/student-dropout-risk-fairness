# Data

## Source
- Dataset: Predict Students' Dropout and Academic Success
- Link: https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success
- Creators: Valentim Realinho, Mónica Vieira Martins, Jorge Machado, Luís Baptista (Polytechnic Institute of Portalegre, Portugal)
- License: CC BY 4.0 (free to use with credit)
- Citation: Realinho, V., Vieira Martins, M., Machado, J., & Baptista, L. (2021). Predict Students' Dropout and Academic Success [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5MC89

## How to get it
1. Go to the UCI link above and click **Download**.
2. Unzip the file in your Downloads folder.
3. data.csv is included in this repo (allowed under CC BY 4.0 with credit) so the Streamlit app can run online.

Note: the file uses semicolons, so load it with `pd.read_csv('data.csv', sep=';')`. Some column names have extra spaces or tabs, so clean them with `df.columns = df.columns.str.strip()`.

## Size
4,424 students (rows) and 37 columns (36 features + Target). No missing values in the key columns below.

## Data dictionary (key columns)
| Column | What it means | Values |
|---|---|---|
| Target | Student's outcome at the end of the normal length of the course | Dropout, Enrolled, Graduate |
| Tuition fees up to date | Whether the student has paid tuition on time | 1 = yes, 0 = no |
| Debtor | Whether the student owes money to the school | 1 = yes, 0 = no |
| Scholarship holder | Whether the student has a scholarship | 1 = yes, 0 = no |
| Age at enrollment | Student's age when they started | 17 to 70 (years) |
| Gender | Student's gender | 1 = male, 0 = female |
| Displaced | Whether the student moved away from home for school | 1 = yes, 0 = no |
| International | Whether the student is from another country | 1 = yes, 0 = no |
| Mother's qualification | Mother's highest education level | Number code (see UCI page for the list) |
| Father's qualification | Father's highest education level | Number code (see UCI page for the list) |
| Curricular units 1st sem (approved) | Number of courses passed in semester 1 | 0 to 26 |
| Curricular units 1st sem (grade) | Average grade in semester 1 | 0 to 20 scale (0 often means no grades) |

## Limitations
- No race column, so the model can't be checked for fairness by race.
- The data comes from one school in Portugal, so results may not apply to US colleges.
- Parents' education is stored as codes, so "first-generation" has to be built by hand and depends on which codes count as college.
- Gender only has two values, so it doesn't capture all students.
