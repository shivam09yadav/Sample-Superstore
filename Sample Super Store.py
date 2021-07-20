#!/usr/bin/env python
# coding: utf-8

# # Information

#  SHIVAM YADAV
# * Data Science & Business Analytics Tasks.
# * TASK 3
# * Exploratory Data Analysis - Retail
# * Perform ‘Exploratory Data Analysis’ on dataset ‘SampleSuperstore’
# * As a business manager, try to find out the weak areas where you can     work to make more profit.
# * Dataset: https://bit.ly/3i4rbWl

# # Import libraries and load dataset

# In[1]:


#!pip install mplcursors
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import mplcursors
matplotlib.use('nbAgg',warn=False, force=True)
import seaborn as sns

df=pd.read_csv("C:\\Users\\shiva\\OneDrive\\Desktop\\Sparks Foundation\\Task 3\SampleSuperstore.csv")
df


# # Drop unwanted columns

# In[2]:


df=df.drop(columns=['Ship Mode','Country','Postal Code','Segment'])
df.head()


# # Get insights about dataset

# In[3]:


df.describe()


# In[4]:


df.info()


# # Find sales for each cateory and subcategory

# In[5]:


sales_df = df.groupby('Category', as_index=False)['Sales'].sum()
subcat_df = df.groupby(['Category','Sub-Category'])['Sales'].sum()
subcat_df['Sales']=map(int,subcat_df)
sales_df


# # Visualising sales for each category and subcategory.
# 

# In[6]:


fig,ax = plt.subplots(figsize=(10,5))
ax.bar(sales_df['Category'],sales_df['Sales'],color='grey',edgecolor='blue',width=0.3) 
ax.set_title(label="Sales for each Category and sub-category", loc='center', pad=None)
ax.set_ylabel('Sales')
ax.set_xlabel('Category')
crs=mplcursors.cursor(ax,hover=True)
@crs.connect("add")
def on_add(sel):
    x, y, width, height = sel.artist[sel.target.index].get_bbox().bounds
    pos=int(x+width/2)
    if pos == 0:
        text=''
        for i in range(4):
            text=text+'\n'+subcat_df.index[i][1]+':'+str(int(subcat_df[i]))
    elif pos == 1:
        text=''
        for i in range(9):
            text=text+'\n'+subcat_df.index[i+4][1]+' : '+str(int(subcat_df[i]))
    else:
        text=''
        for i in range(4):
            text=text+'\n'+subcat_df.index[i+13][1]+':'+str(int(subcat_df[i]))
    
    sel.annotation.set(text=text, position=(pos, 70000))
    sel.annotation.xy = (x + width / 2, y + height)


# ## Subcategories and their sales can be seen upon hovering the respective Categories.
# 
# 
# ### Find profits for each state

# In[7]:


prof_df = df.groupby('State', as_index=False)['Profit'].sum()
prof_df.head()


# ## The graph shows us the overall profit as well as loss (negative values) for each state. The profit/loss is calculated by adding individual values for each state.

# In[8]:


fig,ax = plt.subplots(figsize=(10,6))
ax.bar(prof_df['State'],prof_df['Profit'],color='yellow',edgecolor='green') 
ax.set_title(label="Total Profit for each State", loc='center', pad=None)
ax.set_ylabel('Profit')
ax.set_xlabel('State')
ax.set_xticklabels(prof_df['State'],rotation=90)
plt.tight_layout();


# ## This plot shows us the range of profit for each discount value. The maximum, minimum as well as median range for each discount value is shown. (Outliers are not shown for better visualisation)
# 

# In[9]:


props = dict(boxes="c", medians="black", caps="black")
df.boxplot(by='Discount', column='Profit',showfliers=False,figsize=(10,6),patch_artist=True,color=props)


# # Now lets start Analysing Loss based on various factors
# 
# ### 1. Based on State
# ### First we will get all the states which faced loss and find their total profit/loss across all items

# In[10]:


state_neg=prof_df.loc[prof_df.Profit < 0]
state_neg


# In[11]:


fig,ax = plt.subplots(figsize=(10,5))
def plot_state(ax):
    ax.bar(state_neg['State'],state_neg['Profit'],color='pink',edgecolor='black') 
#ax.legend(label, loc='upper center', fontsize='large',edgecolor='black', borderpad=1.0, shadow=True, handlelength=0)
    ax.set_title(label="States which faced Loss", loc='center', pad=None)
    ax.set_ylabel('Loss')
    ax.set_xlabel('States')
plot_state(ax)
plt.tight_layout()


# ### Here we have visualised loss faced by various states. We can thus get the states which needs better deals to earn profit like:
# #### 1. TEXAS
# #### 2. OHIO
# #### 3. PENNSYLVANIA
# #### 4. ILLINOIS

# # -----------------------------------------------------------------------------

# ## 2. Based on Region
# #### We will find the count of losses faced by various states and visualise them based on their Region.

# In[12]:


state_neg2=df.loc[df.Profit < 0].reset_index(drop=True)
state_pos2=df.loc[df.Profit >= 0].reset_index(drop=True)
dft=state_neg2.groupby(['Region','State'], as_index=False)['Profit'].count()
dft=dft[dft.Profit > 40]
dft


# In[13]:


fig,ax = plt.subplots(figsize=(10,6))
def plot_region(ax):
    d={'Central':'#87CEFA','East':'#6AFB92','South':'#E3F9A6','West':'#FED8B1'}
    dft['color'] = dft['Region'].map(d)
    sns.barplot(data=dft, x=dft.State, y='Profit', hue='Region', palette=d, dodge=False, edgecolor='black')
    ax.set_xticklabels(dft['State'],rotation=90)
    ax.set_title(label="Number of items faced loss in each state (Divided by Region)", loc='center', pad=None)
    ax.set_ylabel('Count')
    ax.set_xlabel('State')
    ax.legend(loc=1, fontsize='large',edgecolor='black', borderpad=1.0, title="Region", shadow=True)
    plt.show()
plot_region(ax)
plt.tight_layout()


# ### It can be seen that regions like CENTRAL and East have maximum loss count along with the specific states in that region.

# # -----------------------------------------------------------------------------
# ## 3. Based on Category
# ### Now we will plot total number of items belonging to each category which faced loss

# In[14]:


state_pos2['Discount'].value_counts().reindex(df.Discount.unique(), fill_value=0).sort_values()
state_neg2['Discount'].value_counts().reindex(df.Discount.unique(), fill_value=0)
state_pos2.head()


# In[15]:


fig,ax = plt.subplots(figsize=(10,5))
def plot_cat(ax):
    dftn=state_neg2.groupby('Category', as_index=False)['Profit'].count()
    ax.bar(dftn['Category'],dftn['Profit'],color='#00FFFF',edgecolor='black',width=0.3)
    ax.set_title(label="Count of items in each category which faced loss", loc='center', pad=None)
    ax.set_ylabel('Count')
    ax.set_xlabel('Category')
plot_cat(ax)
plt.show()


# ### It can be seen that maximum items belonging to OFFICE SUPPLIES category have faced loss followed by FURNITURE
# #### Now lets find the effect of Profit and Discount on each Category

# In[16]:


fig,ax = plt.subplots(figsize=(10,5))
def plot_disccat(ax):
    sns.scatterplot(x="Discount", y="Profit", data=df, hue="Category",ax=ax,s=200,palette='YlOrRd',edgecolor='#C38EC7')
    ax.legend(loc=1, fontsize='large',edgecolor='black', borderpad=1.0, shadow=True)
    ax.set_title('Profit achieved by each Category for each Discount value.')
plot_disccat(ax)
plt.show()


# ### It can be seen that OFFICE SUPPLIES has faced maximum loss due to giving high discount (of 0.8) many times. Whereas other categories are profitable with low discounts.
# # -----------------------------------------------------------------------------
# ### 4. Based on Discount
# #### Now we will find the count of discounts offered where the company faced profit and loss respectively.

# In[17]:


fig,((ax1,ax2)) = plt.subplots(nrows=1, ncols=2,figsize=(10,6))
def plot_disc(ax,x):
    x['Discount'].value_counts().plot(kind = 'bar',color='#00FA9A',edgecolor='black',ax=ax)
    ax.set_xlabel('Discount')
    plt.show()
plot_disc(ax1,state_neg2)
plot_disc(ax2,state_pos2)
ax1.set_ylabel('Loss count')
ax1.set_title(label="Count of discounts offered where\n store faced Loss", loc='center', pad=None)
ax2.set_title(label="Count of discounts offered where\n store faced Profit", loc='center', pad=None)
ax2.set_ylabel('Profit count')


# ## It can be seen that higher the Discount, higher is the Loss count.
# # DASHBOARD
# ### Now lastly we will plot these graphs together which can help us determine some areas requiring improvement.¶

# In[18]:


fig,((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2, ncols=2,figsize=(11,6))
plot_state(ax1)
plot_disc(ax2,state_neg2)
plot_cat(ax3)
#plot_disccat(ax4)
sns.scatterplot(x="Discount", y="Profit", data=df, hue="Category",ax=ax4,s=50,palette='YlOrRd',edgecolor='brown')

ax1.set_xticklabels(state_neg['State'],rotation=80)
#ax4.set_xticklabels(dft['State'],rotation=45,fontsize='small')
ax4.legend(loc=1,fontsize=7,edgecolor='black', shadow=True)
ax2.set_title(label="Count of discounts offered where\n store faced Profit", loc='center', pad=None)
ax3.set_title(label="Count of items in each category\n which faced loss", loc='center', pad=None)
ax4.set_title('Profit achieved by each Category\n for each Discount value.')


plt.tight_layout()


# ### As seen in the graphs we can conclude that we neeed to work on states like Texas, Ohio, Pennsylvania, Illinois and also on Office Supplies Category.
# ### Giving discount of 0.2 yields maximum times Loss(500). But the profit count of it is exeptionally high (nearly 3000) too. Also for discounts < 0.2 loss count is low.
# ### Hence it can be concluded that giving high discounts can lead to Loss.
# ## Solutions:
# ### 1. Giving low discount ( < 15%) on Office Sales products.
# ### 2. Advertising and improvising sales in some Central and Eastern states like Texas and Ohio using low discount, great deals etc.
