# Luxury Housing Market Analytics — Bangalore

This project analyzes the luxury real estate market in Bangalore using Python, MySQL, and Power BI to uncover trends in pricing, demand, buyer patterns, builder performance, and booking conversions.

## Objective
- To clean, transform, and analyze luxury housing market data for insights.
- To identify trends in buyer behavior, pricing, and developer performance.

## Tech Stack
- Python (Pandas, NumPy)
- MySQL
- Power BI
- Statistical Techniques (IQR, Median Imputation)

## Data Cleaning
Performed using Python:
- Column normalization
- Currency conversion
- Missing value imputation
- Outlier treatment using IQR
- Duplicate handling
- Date formatting

## Data Migration
Cleaned dataset was inserted into MySQL for validation and BI consumption.

## SQL Validation
Validated using:
- COUNT(*)
- GROUP BY booking status
- AVG ticket price per builder

## EDA Findings
- Whitefield & Sarjapur lead bookings
- 3BHK is most demanded configuration
- Amenities impact conversion rate
- Direct sales outperform broker channels

## Feature Engineering
Engineered features:
- booking_conversion_rate
- total_ticket_value
- quarter_bucket

## Statistical Techniques
- IQR Outlier Capping: preserves data distribution
- Median Imputation: handles skewed data

## Power BI Insights
Answered 10 business questions covering:
- Market trends
- Builder revenue
- Amenity impact
- Booking conversion
- Top performer scorecards

## Business Insights
- Eastern micro-markets dominate luxury demand
- Higher amenities boost conversion
- Direct channel best for premium buyers

## Deliverables
- Cleaned dataset
- SQL validation results
- Power BI dashboard
- PPT Presentation
- End-to-end documentation

## Conclusion
Luxury housing demand in Bangalore remains strong, driven by connectivity, amenities, and developer brand value.
