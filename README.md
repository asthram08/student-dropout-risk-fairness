# Who Should a College Help First?

**A college advising office can only reach out to a limited number of students each semester. Who should they help first, and is the AI that decides fair?**

## Why this matters
Advisors have limited time, so colleges increasingly use prediction tools to decide which students to contact. These tools can help, but they can also do harm. In 2023, The Markup found that Wisconsin's Dropout Early Warning System labeled many students "high risk" who went on to graduate, and its false alarms fell much more heavily on Black and Hispanic students.

This project builds a dropout risk model and then goes further. It turns predictions into an outreach plan (who to contact first and what kind of help they need) and audits whether the model treats some student groups unfairly.

## Research questions
1. **Who drops out?** Which background, money, and grade factors differ most between students who leave and those who stay?
2. **How early can we tell?** How accurate is the model at enrollment (no grades yet) vs. after the first semester?
3. **Which model works best?** A simple baseline vs. logistic regression vs. random forest.
4. **Is it fair?** Does the model wrongly flag, or miss, some groups more often than others?
5. **Who should the college help first, and how?** A ranked outreach list and a type of help for each group.

## Data
[Predict Students' Dropout and Academic Success](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success) from the UCI Machine Learning Repository: 4,424 students from a university in Portugal, 36 features, and three outcomes (Dropout, Enrolled, Graduate). License: CC BY 4.0. See [data/README.md](data/README.md) for download steps and the data dictionary.

**First look:** about 32% of students dropped out, 50% graduated, and 18% were still enrolled. The model will predict **dropout vs. not dropout**, like real early warning tools.

## Tools
Python, pandas, NumPy, SQL (SQLite), Matplotlib, Seaborn, scikit-learn, SHAP, Fairlearn, Streamlit

## Project structure
data/ download steps and data dictionary
notebooks/ 01 explore, 02 model, 03 fairness, 04 outreach plan
app/ Streamlit app


## Status
- [x] Setup and first look at the data
- [ ] Exploration (SQL + charts)
- [ ] Models
- [ ] Fairness check
- [ ] Outreach plan
- [ ] Streamlit app

## Limitations
- The data has no race column, so the model can't be checked for fairness by race.
- The data comes from one school in Portugal, so results may not apply to US colleges.

## Sources
- Realinho, V., Vieira Martins, M., Machado, J., & Baptista, L. (2021). Predict Students' Dropout and Academic Success. UCI Machine Learning Repository. https://doi.org/10.24432/C5MC89
- The Markup (2023). [False Alarm: How Wisconsin Uses Race and Income to Label Students "High Risk"](https://themarkup.org/machine-learning/2023/04/27/false-alarm-how-wisconsin-uses-race-and-income-to-label-students-high-risk)
