from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/processed/titanic_cleaned.csv'

def load(): return pd.read_csv(DATA)

def test_no_duplicates(): assert load().duplicated().sum()==0

def test_unique_key():
    df=load()
    assert df['PassengerId'].is_unique
    assert df['PassengerId'].notna().all()

def test_categories():
    df=load()
    assert set(df['Survived'].unique()).issubset({0,1})
    assert set(df['Pclass'].unique()).issubset({1,2,3})
    assert set(df['Sex'].unique()).issubset({'male','female'})
    assert set(df['Embarked'].unique()).issubset({'S','C','Q'})

def test_ranges():
    df=load()
    assert df['Age'].between(0,100).all()
    assert (df['Fare']>=0).all()
