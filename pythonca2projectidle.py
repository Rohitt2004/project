import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "C:/Users/rohit/Downloads/datasetpython.csv"
df = pd.read_csv(file_path, encoding='utf-8')  

df.info()
#Unique elements
df.nunique()

print("Summary statistics of numeric columns:")
print(df.describe())



# Check missing values before handling
print("Missing values before cleaning:")
print(df.isnull().sum())

# List of numeric and non-numeric columns based on WHO dataset structure
numeric_cols = [
    'year', 'pm10_concentration', 'pm25_concentration', 'no2_concentration',
    'pm10_tempcov', 'pm25_tempcov', 'no2_tempcov', 'population',
    'latitude', 'longitude', 'who_ms'
]

non_numeric_cols = [
    'who_region', 'iso3', 'country_name', 'city', 'type_of_stations',
    'reference', 'web_link', 'population_source'
]

# Fill missing numeric columns with their mean
for col in numeric_cols:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].mean())

# Fill missing non-numeric columns with their mode
for col in non_numeric_cols:
    if col in df.columns and df[col].isna().any():
        mode_value = df[col].mode()
        if not mode_value.empty:
            df[col] = df[col].fillna(mode_value[0])

# Confirm that missing values are handled
print("\nMissing values after cleaning:")
print(df.isnull().sum())

# Loop through all object (categorical/text) columns
print("LOOP THROUGH ALL OBJECT")
for col in df.select_dtypes(include='object').columns:
    unique_count = df[col].nunique()
    print(f"{col}: {unique_count} unique value{'s' if unique_count > 1 else ''}")




    # Print the current column names to verify structure
print("Final Column Names in the Dataset:")
print(df.columns)





print("Filter data for India")
india_data = df[df['country_name'] == 'India']

# Group by year and calculate mean concentration for each pollutant
pollution_trend = india_data.groupby('year')[
    ['pm25_concentration', 'pm10_concentration', 'no2_concentration']
].mean().reset_index()

# Plotting
plt.figure(figsize=(12, 6))
sns.lineplot(data=pollution_trend, x='year', y='pm25_concentration', label='PM2.5', marker='o')
sns.lineplot(data=pollution_trend, x='year', y='pm10_concentration', label='PM10', marker='s')
sns.lineplot(data=pollution_trend, x='year', y='no2_concentration', label='NO₂', marker='^')

plt.title('Air Pollution Trends in India (2010–2022)', fontsize=14)
plt.xlabel('Year')
plt.ylabel('Concentration (µg/m³)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()




print(df.columns)

india_2020 = df[(df['year'] == 2020) & (df['country_name'] == 'India')]

top_cities = india_2020.sort_values(by='pm25_concentration', ascending=False).head(10)

top_cities = top_cities.dropna(subset=['pm25_concentration', 'city'])  # Replace 'city' with the correct column name

# Plotting
plt.figure(figsize=(10, 6))
sns.barplot(x='pm25_concentration', y='city', data=top_cities, palette='coolwarm')  # Replace 'city' if needed

# Customization
plt.title('Top 10 Most Polluted Cities in India (2020)', fontsize=14)
plt.xlabel('PM2.5 Concentration (µg/m³)')
plt.ylabel('City')
plt.tight_layout()
plt.show()

# Drop rows with missing region or pollutant values
df = df.dropna(subset=['who_region', 'pm25_concentration', 'pm10_concentration', 'no2_concentration'])

# Group by WHO region and calculate mean concentrations
region_avg = df.groupby('who_region')[
    ['pm25_concentration', 'pm10_concentration', 'no2_concentration']
].mean().reset_index()

# Reshape the data for seaborn (from wide to long)
region_melted = region_avg.melt(id_vars='who_region',
                                var_name='Pollutant',
                                value_name='Concentration')

# Plotting
plt.figure(figsize=(12, 6))
sns.barplot(data=region_melted, x='who_region', y='Concentration', hue='Pollutant', palette='Set2')

# Customize the plot
plt.title('Average Pollutant Levels by WHO Region', fontsize=14)
plt.xlabel('WHO Region')
plt.ylabel('Average Concentration (µg/m³)')
plt.xticks(rotation=30)
plt.legend(title='Pollutant')
plt.tight_layout()
plt.show()

print("FILL MISSING VALUES")
# Fill missing PM2.5 values with mean
df['pm25_concentration'] = df['pm25_concentration'].fillna(df['pm25_concentration'].mean())

# Group by year to get average PM2.5 for India and Global
avg_pm25_india = df[df['country_name'] == 'India'].groupby('year')['pm25_concentration'].mean()
avg_pm25_global = df.groupby('year')['pm25_concentration'].mean()

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(avg_pm25_india.index, avg_pm25_india.values, label='India', marker='o', linewidth=2, color='crimson')
plt.plot(avg_pm25_global.index, avg_pm25_global.values, label='Global Average', marker='o', linewidth=2, color='steelblue')

plt.title('PM2.5 Trends Over Years: India vs Global', fontsize=14)
plt.xlabel('Year')
plt.ylabel('PM2.5 Concentration (µg/m³)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title='Region')
plt.tight_layout()
plt.show()



# Filter data for Kolkata in 2020
city_name = 'Kolkata'
year_filter = 2020

city_data = df[
    (df['country_name'] == 'India') &
    (df['city'].str.lower().str.contains(city_name.lower())) &
    (df['year'] == year_filter)
]

# Check if data exists
if not city_data.empty:
    # Get the first matching row for pollutant concentrations
    values = city_data[['pm25_concentration', 'pm10_concentration', 'no2_concentration']].iloc[0]
    labels = ['PM2.5', 'PM10', 'NO₂']
    
    # Plot pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=['crimson', 'orange', 'purple'])
    plt.title(f'Pollution Composition in {city_name.title()} - {year_filter}')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
else:
    print(f"No data available for {city_name} in {year_filter}.")

# Pivot table to get average pollutant concentrations by country
pivot_df = df.pivot_table(
    index='country_name', 
    values=['pm25_concentration', 'pm10_concentration', 'no2_concentration'], 
    aggfunc='mean'
)

# Sort by PM2.5 and get top 20 polluted countries
pivot_df_top = pivot_df.dropna().sort_values(by='pm25_concentration', ascending=False).head(20)

# Plotting the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_df_top, annot=True, cmap='YlOrRd', fmt=".1f")
plt.title('Pollutant Concentration by Country (Top 20 by PM2.5)')
plt.xlabel('Pollutant')
plt.ylabel('Country')
plt.tight_layout()
plt.show()




# Generate correlation matrix from numeric columns
correlation_matrix = df.select_dtypes(include='number').corr()

# Plotting the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", square=True)
plt.title('Correlation Matrix of Numeric Features')
plt.tight_layout()
plt.show()
