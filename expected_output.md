## output/customers.csv
customer_id,name,username,email,email_domain,phone,city,zipcode,latitude,longitude,company,website
<int>,<text>,<text>,<email>,<tld>,<text>,<text>,<text>,<float>,<float>,<text>,<text>

## output/city_counts.csv
city,customer_count
<text>,<int>
... (sorted by customer_count descending, then city)

## Console findings
Customers retrieved : <n>
Unique cities       : <n>
Most common city    : <city> (<n>)
Email domains       : {<tld>: <n>, ...}
Chart saved to      : output/customer_distribution.png

## output/customer_distribution.png
A titled bar chart, one bar per category, axes labelled, readable tick labels.
