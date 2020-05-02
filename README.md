Goal : To plot a zipcode level map of restaurant cuisines in LA

### Data sources


### Scripts

**0_jsonize_tsv.py**

Converts tab separated values downloaded from LA Health inspection website to a json format indexed by field names in the header.
The same can be achieved using Pandas but is not necessary

**1_plot_inspections_data_on_maps.py**

Simple plot example using folium choropleths to plot keyword frequency on names from inspections data.

**2_sort_by_restaurants.py**

Rearranges inspections data by restaurants aggregating multiple inspections at the same restaurants.
This will be used to query the Yelp Fusion API.

**3_plot_zipcode_catgories.py**

Plots a choropleth of majority cuisine in each zip code, highlighted by color.
Cuisine information is shown on a tooltip.

**4_get_restaurant_details.py**

Downloads restaurant data from Yelp Fusion API. These can be used to create 


**yelputil.py**

Python wrapper for the Yelp HTTP API. Functions are provided for finding restaurants by name, address and listing their details once found.
