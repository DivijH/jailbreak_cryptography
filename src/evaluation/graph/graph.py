import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

table_gpt = {
    'Keyboard' : {
        'Cyber Security': 23.076923076923077,
        'Terrorism':  0.0,
        'Drugs': 0.0,
        'Murder': 0.0,
        'Identity Theft': 100.0,
        'Violence': 0.0,
        'Financial': 25.0,
        'Misinformation': 25.0,
        'Self-Harm': 0.0,
        'Theft': 20.0,
        'Hate Speech': 33.33333333333333,
        'Adult Content': 0.0,
        'Stalking': 0.0,
        'Libel': 0.0
    },
    'Upside-Down': {
        'Cyber Security': 30.76923076923077,
        'Terrorism': 33.33333333333333,
        'Drugs': 0.0,
        'Murder': 100.0,
        'Identity Theft': 0.0,
        'Violence': 0.0,
        'Financial': 25.0,
        'Misinformation': 50.0,
        'Self-Harm': 0.0,
        'Theft': 20.0,
        'Hate Speech': 0.0,
        'Adult Content': 100.0,
        'Stalking': 0.0,
        'Libel': 50.0
    },
    'Word Rev': {
        'Cyber Security': 46.15384615384615,
        'Terrorism': 66.66666666666666,
        'Drugs': 50.0,
        'Murder': 66.66666666666666,
        'Identity Theft': 0.0,
        'Violence': 33.33333333333333,
        'Financial': 0.0,
        'Misinformation': 75.0,
        'Self-Harm': 0.0,
        'Theft': 40.0,
        'Hate Speech': 0.0,
        'Adult Content': 100.0,
        'Stalking': 0.0,
        'Libel': 0.0
    },
    'Grid': {
        'Cyber Security': 23.076923076923077,
        'Terrorism': 50.0,
        'Drugs': 50.0,
        'Murder': 66.66666666666666,
        'Identity Theft': 0.0,
        'Violence': 33.33333333333333,
        'Financial': 75.0,
        'Misinformation': 25.0,
        'Self-Harm': 50.0,
        'Theft': 0.0,
        'Hate Speech': 33.33333333333333,
        'Adult Content': 100.0,
        'Stalking': 0.0,
        'Libel': 50.0
    },
    'Word Sub': {
        'Cyber Security': 69.23076923076923,
        'Terrorism': 33.33333333333333,
        'Drugs': 50.0,
        'Murder': 100.0,
        'Identity Theft': 100.0,
        'Violence': 33.33333333333333,
        'Financial': 75.0,
        'Misinformation': 0.0,
        'Self-Harm': 0.0,
        'Theft': 60.0,
        'Hate Speech': 33.33333333333333,
        'Adult Content': 0.0,
        'Stalking': 0.0,
        'Libel': 0.0
    }
}


table = {
'Keyboard' : {
        'Cyber Security': 0,
        'Terrorism':  16.67,
        'Drugs': 0.0,
        'Murder': 0.0,
        'Identity Theft': 0.0,
        'Violence': 0.0,
        'Financial': 0.0,
        'Misinformation': 0.0,
        'Self-Harm': 0.0,
        'Theft': 00.0,
        'Hate Speech': 0,
        'Adult Content': 0.0,
        'Stalking': 0.0,
        'Libel': 0.0
    },
    'Upside-Down': {
        'Cyber Security': 38.461,
        'Terrorism': 16.67,
        'Drugs': 50.0,
        'Murder': 33.33,
        'Identity Theft': 0.0,
        'Violence': 33.3,
        'Financial': 0.0,
        'Misinformation': 0.0,
        'Self-Harm': 0.0,
        'Theft': 40.0,
        'Hate Speech': 0.0,
        'Adult Content': 0.0,
        'Stalking': 0.0,
        'Libel': 0.0
    },
    'Word Rev': {
        'Cyber Security': 76.923,
        'Terrorism': 66.66666666666666,
        'Drugs': 100.0,
        'Murder': 100,
        'Identity Theft': 0.0,
        'Violence': 33.33333333333333,
        'Financial': 50.0,
        'Misinformation': 75.0,
        'Self-Harm': 0.0,
        'Theft': 80.0,
        'Hate Speech': 33.333,
        'Adult Content': 100.0,
        'Stalking': 100.0,
        'Libel': 50.0
    },
    'Grid': {
        'Cyber Security': 7.692,
        'Terrorism': 0.0,
        'Drugs': 0.0,
        'Murder': 33.33,
        'Identity Theft': 100.0,
        'Violence': 0,
        'Financial': 0,
        'Misinformation': 0,
        'Self-Harm': 0,
        'Theft': 0.0,
        'Hate Speech': 33.33333333333333,
        'Adult Content': 0.0,
        'Stalking': 0.0,
        'Libel': 50.0
    },
    'Word Sub': {
        'Cyber Security': 92.308,
        'Terrorism': 66.667,
        'Drugs': 0,
        'Murder': 66.667,
        'Identity Theft': 100.0,
        'Violence': 66.667,
        'Financial': 50.0,
        'Misinformation': 75.0,
        'Self-Harm': 0.0,
        'Theft': 80.0,
        'Hate Speech': 33.33333333333333,
        'Adult Content': 0.0,
        'Stalking': 0.0,
        'Libel': 100.0
    }
}


# Create a DataFrame from the table
df = pd.DataFrame(table)
df = df.loc[df.mean(axis=1).sort_values(ascending=False).index]

# Set the figure size
plt.figure(figsize=(12, 8))
plt.xticks(rotation=0, fontsize=20)
plt.yticks(fontsize=20)

# Create the heatmap with red color scale
sns.heatmap(df, annot=True, fmt=".1f", cmap='Reds', annot_kws={"size": 20})

# Set title and labels
plt.xlabel('Ciphers', fontsize=20)

plt.savefig('cipher_heatmap_gemini.pdf', bbox_inches='tight')
plt.close()