# %%
import pandas as pd
import matplotlib.pyplot as plt


# %%
data = pd.read_csv('test_history.csv')
data.head()

# %%
data

# %%
data.dtypes

# %%
committer_grp = data.groupby('committer').sum()

# %%
committer_grp

# %%


# %%
committer_grp.plot(legend=True,kind='bar',figsize=(20,18))

# %%
#2002-01-02 04:56:19+00:00	
data['commit date'] = pd.to_datetime(data['commit date'],format='%Y-%m-%d %H:%M:%S',utc=True)

# %%
data

# %%
data['commit_year'] = data['commit date'].dt.year
data['commit_month'] = data['commit date'].dt.month

# %%
data

# %%
year_grp = data.groupby('commit_year')['number of major contributors','number of minor contributors','number of commits to file'].sum()
year_grp2 = data.groupby('commit_year')['number of minor contributors','number of major contributors'].sum()
year_grp3 = data.groupby('commit_year')['number of commits to file'].sum()


# %%
def Fig1() :
    Figure_1 = year_grp2.plot(figsize=(15,8))
    plt.title("Major Contributors vs Year")
    plt.xlabel("Year")
    plt.xlim(left=2005)
    plt.xticks(rotation='vertical')
    plt.ylabel("Activity Number")
    plt.savefig("Figure_1.png", format="png") 
    plt.show()
    plt.close()
# %%
def Fig2() :
    Figure_2 = data['change type'].value_counts().plot(kind='pie',legend=True, label="")
    plt.title("Contributor Actions")
    plt.savefig("Figure_2.png", format="png") 
    plt.show()
    plt.close()
# %% [markdown]
# Top 10 number of major contributors

# %%
def Fig3() :
    Figure_3 = committer_grp['number of major contributors'].nlargest(10).plot(kind='bar',figsize=(18,12))
    plt.title("Top 10 Authors against number of major contributions")
    plt.xlabel("Author Names")
    plt.ylabel("Number of Major Contributions")
    plt.savefig("Figure_3.png", format="png") 
    plt.show()
    plt.close()
# %% [markdown]
# Top 10 number of minor contributors

# %%
def Fig4() :
    Figure_4 = committer_grp['number of minor contributors'].nlargest(10).plot(kind='bar',figsize=(18,12))
    plt.title("Top 10 Authors against number of minor contributions")
    plt.xlabel("Author Names")
    plt.ylabel("Number of Minor Contributions")
    plt.savefig("Figure_4.png", format="png") 
    plt.show()
    plt.close()
# %% [markdown]
# Top 10 number of commits to file

# %%
def Fig5() :
    Figure_5 = (committer_grp['number of commits to file'].nlargest(10).plot(kind='bar',figsize=(18,12)))
    plt.title("Top 10 Authors against Total number of contributions")
    plt.xlabel("Author Names")
    plt.ylabel("Number of Total contributions")
    plt.savefig("Figure_5.png", format="png") 
    plt.show()
    plt.close()

def Fig6() :
    Figure_6 = year_grp3.plot(figsize=(15,8))
    plt.title("Number of Committs vs Year")
    plt.xlabel("Year")
    plt.ylabel("Number of Committs")
    plt.xlim(left=2005)
    plt.savefig("Figure_6.png", format="png") 
    plt.show()
    plt.close()

Fig1()
Fig2()
Fig3()
Fig4()
Fig5()
Fig6()