# Advanced Historical Data Processing with CSV
# This file demonstrates reading, processing, and analyzing CSV data

import csv
from datetime import datetime

def create_sample_data():
    """Create a sample CSV file with historical trade data"""
    trade_data = [
        ["Year", "Country", "Trade_Partner", "Export_Value", "Import_Value", "Trade_Type"],
        [1850, "Britain", "India", 12500000, 8750000, "Colonial"],
        [1850, "Britain", "China", 8200000, 15600000, "International"],
        [1850, "France", "Algeria", 3400000, 1200000, "Colonial"],
        [1860, "Britain", "India", 15600000, 11200000, "Colonial"],
        [1860, "Britain", "China", 9800000, 18900000, "International"],
        [1860, "France", "Algeria", 4100000, 1800000, "Colonial"],
        [1860, "USA", "Britain", 18500000, 22100000, "International"],
        [1870, "Britain", "India", 19200000, 14500000, "Colonial"],
        [1870, "Britain", "China", 11400000, 21200000, "International"],
        [1870, "France", "Algeria", 5200000, 2400000, "Colonial"],
        [1870, "USA", "Britain", 25600000, 31200000, "International"],
        [1870, "USA", "France", 8900000, 12300000, "International"],
        [1880, "Britain", "India", 24800000, 18900000, "Colonial"],
        [1880, "Britain", "China", 13600000, 24500000, "International"],
        [1880, "Germany", "USA", 15200000, 18700000, "International"]
    ]
    
    with open('historical_trade.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(trade_data)
    
    print("Sample CSV file 'historical_trade.csv' created!")

class HistoricalTradeAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.data = []
        self.load_data()
    
    def load_data(self):
        """Load CSV data into memory"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Convert numeric columns
                    row['Year'] = int(row['Year'])
                    row['Export_Value'] = int(row['Export_Value'])
                    row['Import_Value'] = int(row['Import_Value'])
                    row['Trade_Balance'] = row['Export_Value'] - row['Import_Value']
                    self.data.append(row)
            print(f"Loaded {len(self.data)} trade records from {self.filename}")
        except FileNotFoundError:
            print(f"File {self.filename} not found. Creating sample data...")
            create_sample_data()
            self.load_data()
    
    def analyze_by_country(self, country):
        """Analyze trade data for a specific country"""
        country_data = [row for row in self.data if row['Country'] == country]
        
        if not country_data:
            print(f"No data found for {country}")
            return
        
        print(f"\n{country} Trade Analysis:")
        print("=" * 40)
        
        # Calculate totals by year
        years = {}
        for record in country_data:
            year = record['Year']
            if year not in years:
                years[year] = {'exports': 0, 'imports': 0, 'partners': set()}
            
            years[year]['exports'] += record['Export_Value']
            years[year]['imports'] += record['Import_Value']
            years[year]['partners'].add(record['Trade_Partner'])
        
        print("Year-by-year summary:")
        for year in sorted(years.keys()):
            data = years[year]
            balance = data['exports'] - data['imports']
            print(f"{year}: Exports: ${data['exports']:,}, Imports: ${data['imports']:,}")
            print(f"      Balance: ${balance:,}, Partners: {len(data['partners'])}")
        
        # Growth analysis
        sorted_years = sorted(years.keys())
        if len(sorted_years) > 1:
            first_year = sorted_years[0]
            last_year = sorted_years[-1]
            
            export_growth = ((years[last_year]['exports'] - years[first_year]['exports']) 
                           / years[first_year]['exports'] * 100)
            
            print(f"\nExport growth {first_year}-{last_year}: {export_growth:.1f}%")
    
    def analyze_trade_relationships(self):
        """Analyze trade relationships and patterns"""
        print("\nTrade Relationship Analysis:")
        print("=" * 40)
        
        # Find most active trade relationships
        relationships = {}
        for record in self.data:
            key = f"{record['Country']} - {record['Trade_Partner']}"
            if key not in relationships:
                relationships[key] = []
            relationships[key].append(record)
        
        print("Most active trade relationships:")
        for relationship, records in relationships.items():
            if len(records) >= 3:  # Only show relationships with 3+ records
                total_trade = sum(r['Export_Value'] + r['Import_Value'] for r in records)
                years = [r['Year'] for r in records]
                print(f"• {relationship}: {len(records)} records, ${total_trade:,} total trade")
                print(f"  Years: {min(years)}-{max(years)}")
    
    def colonial_vs_international_trade(self):
        """Compare colonial vs international trade patterns"""
        print("\nColonial vs International Trade:")
        print("=" * 40)
        
        colonial_data = [r for r in self.data if r['Trade_Type'] == 'Colonial']
        international_data = [r for r in self.data if r['Trade_Type'] == 'International']
        
        # Calculate averages
        if colonial_data:
            avg_colonial_exports = sum(r['Export_Value'] for r in colonial_data) / len(colonial_data)
            avg_colonial_balance = sum(r['Trade_Balance'] for r in colonial_data) / len(colonial_data)
        else:
            avg_colonial_exports = avg_colonial_balance = 0
        
        if international_data:
            avg_intl_exports = sum(r['Export_Value'] for r in international_data) / len(international_data)
            avg_intl_balance = sum(r['Trade_Balance'] for r in international_data) / len(international_data)
        else:
            avg_intl_exports = avg_intl_balance = 0
        
        print(f"Colonial Trade ({len(colonial_data)} records):")
        print(f"  Average exports: ${avg_colonial_exports:,.0f}")
        print(f"  Average balance: ${avg_colonial_balance:,.0f}")
        
        print(f"\nInternational Trade ({len(international_data)} records):")
        print(f"  Average exports: ${avg_intl_exports:,.0f}")
        print(f"  Average balance: ${avg_intl_balance:,.0f}")
    
    def generate_report(self):
        """Generate a comprehensive analysis report"""
        print("\n" + "=" * 60)
        print("COMPREHENSIVE HISTORICAL TRADE ANALYSIS REPORT")
        print("=" * 60)
        
        # Basic statistics
        total_records = len(self.data)
        years_covered = set(r['Year'] for r in self.data)
        countries = set(r['Country'] for r in self.data)
        
        print(f"Dataset Overview:")
        print(f"• Total records: {total_records}")
        print(f"• Years covered: {min(years_covered)}-{max(years_covered)}")
        print(f"• Countries: {len(countries)} ({', '.join(sorted(countries))})")
        
        # Analyze each country
        for country in sorted(countries):
            self.analyze_by_country(country)
        
        # Additional analyses
        self.analyze_trade_relationships()
        self.colonial_vs_international_trade()

# Main execution
if __name__ == "__main__":
    print("Historical Trade Data Analysis")
    print("=" * 40)
    
    # Create analyzer and run analysis
    analyzer = HistoricalTradeAnalyzer('historical_trade.csv')
    analyzer.generate_report()
    
    print("\n" + "=" * 60)
    print("Analysis complete! Check the generated report above.")
    print("The sample CSV file has been created for further experimentation.")