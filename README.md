# Final-Project-Statistical-Modelling-with-Python

## Project/Goals
This project aims to analyze the relationship between bike station availability and Points of Interest (POIs) in a specific city. By integrating data from the CityBikes API, Yelp API and FourSquare API, the project explores how POI characteristics (like type and proximity) impact the number of available bikes. This was achieved first by Comparing the quality of the data from the Foursquare and Yelp APIs first. The ultimate goal is to build a regression model to uncover statistical relationships and propose actionable insights. Additionally, the project examines how this regression problem could be reframed as a classification problem.

## Process

### Step 1: Data Collection
1. The project began by collecting bike station data which included their location.
2. This data was then used to query both the Foursquare and Yelp APIs to get a list of POIs in close  proximity to these bike stations.
3. Data was then merged into a single dataframe, which included bike station data as well as the POIs nearest to them.

### Step 2: Data Exploration and Analysis
1. The data was then visualized to look at the relationship between the bike station location and the location of POIs using scatter plots.
2. The quality of both APIs were then evaluated based on several key criteria.
3. Visualized relationships between bike station availability and POI proximity/type using scatterplots, grouped by POI categories.

### Step 3: Statistical Modeling
1. Built a regression model to analyze the impact of POI characteristics on the number of available bikes
2. Interpreted model coefficients and residuals to derive meaningful insights.
3. Conceptualized a classification approach that categorized bike stations based on availability thresholds (e.g., high/low availability).

### Step 4: Results Storage
1. Stored the processed datasets and modeling results in an SQLite3 database, organized in the data/ folder for reproducibility.

## Results
The project revealed the following key results:

*   **API Coverage Comparison:** Through comparison of the Foursquare and Yelp APIs using the `compare_api_quality()` method it was determined that the integration of the CityBikes and Yelp APIs provides a comprehensive view of bike stations and nearby attractions, although some limitations in POI data completeness were observed.

*   **Model Results:** Initial attempts to model the number of bikes at each bike station using variables such as `rating`, `review_count`, and `distance_meters` as predictors were unsuccessful. All variables were determined not to be statistically significant, and the regression model performed poorly, with an R-squared value of 0.292.

## Challenges 
The project faced several challenges, including:

*   **Data Variability:** It was hard to get good data about the ratings of POIs from Foursquare and Yelp. The POI ratings from the APIs were sparse and contained many `N/A` values.
*   **Model Performance:** The regression model struggled to predict bike station usage based on the initial set of chosen features.
* **Assessing Quality** Deciding how to assess the "quality" of an API was a challenge. While number of POIs might be a good measure, other measures might have also been relevant.
*   **Data Cleaning and Formatting:** The initial datasets required substantial preprocessing such as handling missing values.
* **Exploration:** It was a challenge determining the best way to approach the dataset to obtain interesting findings.

## Future Goals
If more time were available, the following would be explored:

*   **Feature Engineering:** Develop more informative and relevant features for the regression model that would improve its predictive performance by looking into the number of POIs for each category instead of using `rating`, `review_count`, and `distance_meters`.
*   **Advanced Modeling Techniques:** Experiment with advanced modeling techniques, such as non-linear regression models, or different types of models.
*  **Better Data:** Obtain better data regarding usage at each of the bike stations, such as number of trips, or more relevant information regarding the bike station itself.
*   **Expand Analysis:** Explore other POI characteristics and incorporate additional data sources, such as weather data, to improve model accuracy and derive more insights.
*   **Classification:** Try to bin the target variable to create a classification model.
*   **Refine the definition of "Quality"**: Define more specific or relevant ways of defining "quality" of a POI.
