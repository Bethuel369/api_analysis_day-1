Pesa Pulse — Customer Data Analysis (Day 1)

Hey there! This repo holds my initial data exploration for Pesa Pulse. Our marketing team is getting ready to launch regional campaigns using a new partner's directory API, so I've pulled the raw JSON data, cleaned it up, and ran some quick breakdowns to answer the big question: where are our customers located, and what does this user base actually look like?

1. My Approach

Here’s how I tackled the data pipeline step-by-step:

Fetching the API Data safely: I used requests to pull from https://jsonplaceholder.typicode.com/users with a 10-second timeout. Instead of letting the script crash with a messy traceback if the Wi-Fi drops or the API is down, I wrapped it in a try-except block to log a clean error message.

Exploring the JSON structure: I wrote a recursive explore() function to print out every key and its data type. This helped me map out nested objects like address and company, and figure out how deep the geo coordinates (lat / lng) were hidden.

Cleaning and flattening: I pulled all relevant fields into flat Python dictionaries. While doing this, I cast coordinate strings to actual float numbers and parsed out the top-level domain (TLD) from email addresses.

Aggregating with plain Python: Before jumping into pandas, I used basic Python tools—set comprehensions for unique cities, dictionary loops for city totals, and dict comprehensions for email domain counts.

Pandas validation & export: I loaded the cleaned records into a pandas DataFrame to double-check my hand-written counts against value_counts() and check data types. Then I exported everything to clean CSVs without index columns.

Visualizing: I plotted the email domain distribution with matplotlib and saved a high-res chart for marketing slides.

2. How to Run This Project

If you want to run the code locally, follow these steps:

Clone the repository:

git clone <your-repo-url>
cd day1-api-analysis


Install the dependencies:

pip install -r requirements.txt


Run the script:

python analysis.py


Check the outputs:
Head over to the output/ folder. You should see:

customers.csv — Full flattened dataset.

city_counts.csv — Summary count of users per city.

customer_distribution.png — Visual chart ready for slides.

3. Key Findings for Marketing

100% City Spread (10 cities across 10 users): Every single customer in this sample lives in a different city. Because of this 1:1 ratio, running localized billboard or city-specific ground events right now won't give us much ROI. Marketing should focus on digital, region-wide campaigns instead.

Commercial & Tech-Leaning Users: .biz was the most common email domain suffix in the dataset (30% of users), followed by tech and web domains like .io, .net, .info, and .org. This suggests our partner's audience consists mostly of tech-savvy individuals and business accounts.

Why Email Domain Chart > City Chart: If I plotted cities, every single bar would just be height 1 (which looks pretty boring on a slide!). Grouping by email domain gave us a much more meaningful picture of user categories.

4. Assumptions Made

API Payload Structure: I assumed the partner API will always return user objects following JSONPlaceholder's standard schema (address, geo, company).

Fallback Values: If latitude or longitude values are missing or invalid, the script defaults them to 0.0.

Domain Parsing: Top-level email domains are assumed to be everything after the final dot in the user's email address.