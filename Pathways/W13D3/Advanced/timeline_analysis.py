# Advanced Historical Timeline Analysis
# This file combines all previous concepts for comprehensive historical analysis

import csv
from datetime import datetime
import json

class HistoricalEvent:
    """Class to represent a historical event with rich metadata"""
    def __init__(self, name, year, event_type, location, significance, participants=None):
        self.name = name
        self.year = year
        self.event_type = event_type
        self.location = location
        self.significance = significance
        self.participants = participants or []
    
    def __str__(self):
        return f"{self.year}: {self.name} ({self.event_type})"
    
    def to_dict(self):
        """Convert event to dictionary for JSON export"""
        return {
            'name': self.name,
            'year': self.year,
            'type': self.event_type,
            'location': self.location,
            'significance': self.significance,
            'participants': self.participants
        }

class HistoricalTimelineAnalyzer:
    """Advanced analyzer for historical timelines and patterns"""
    
    def __init__(self):
        self.events = []
        self.load_sample_events()
    
    def load_sample_events(self):
        """Load comprehensive sample historical data"""
        sample_events = [
            HistoricalEvent("Fall of Western Roman Empire", 476, "Political", "Rome", 9, 
                          ["Odoacer", "Romulus Augustulus"]),
            HistoricalEvent("Battle of Tours", 732, "Military", "France", 8, 
                          ["Charles Martel", "Abdul Rahman Al Ghafiqi"]),
            HistoricalEvent("Charlemagne Crowned Emperor", 800, "Political", "Rome", 8, 
                          ["Charlemagne", "Pope Leo III"]),
            HistoricalEvent("Norman Conquest of England", 1066, "Military", "England", 9, 
                          ["William the Conqueror", "Harold Godwinson"]),
            HistoricalEvent("First Crusade Begins", 1096, "Religious", "Europe", 7, 
                          ["Pope Urban II", "Peter the Hermit"]),
            HistoricalEvent("Magna Carta Signed", 1215, "Political", "England", 9, 
                          ["King John", "English Barons"]),
            HistoricalEvent("Black Death Begins", 1347, "Social", "Europe", 10, 
                          ["Genoese merchants", "European population"]),
            HistoricalEvent("Fall of Constantinople", 1453, "Military", "Constantinople", 9, 
                          ["Mehmed II", "Constantine XI"]),
            HistoricalEvent("Columbus Reaches Americas", 1492, "Exploration", "Caribbean", 10, 
                          ["Christopher Columbus", "Spanish Crown"]),
            HistoricalEvent("Protestant Reformation Begins", 1517, "Religious", "Germany", 9, 
                          ["Martin Luther", "Catholic Church"]),
            HistoricalEvent("Spanish Armada Defeated", 1588, "Military", "English Channel", 8, 
                          ["Elizabeth I", "Philip II of Spain"]),
            HistoricalEvent("Thirty Years' War Begins", 1618, "Military", "Europe", 8, 
                          ["Ferdinand II", "Frederick V"]),
            HistoricalEvent("English Civil War Begins", 1642, "Political", "England", 8, 
                          ["Charles I", "Parliament"]),
            HistoricalEvent("Peace of Westphalia", 1648, "Political", "Europe", 8, 
                          ["European Powers", "Holy Roman Empire"]),
            HistoricalEvent("Great Fire of London", 1666, "Natural", "London", 6, 
                          ["London citizens", "Samuel Pepys"]),
            HistoricalEvent("Glorious Revolution", 1688, "Political", "England", 8, 
                          ["William of Orange", "James II"]),
            HistoricalEvent("War of Spanish Succession", 1701, "Military", "Europe", 7, 
                          ["Louis XIV", "European Coalition"]),
            HistoricalEvent("Seven Years' War Begins", 1756, "Military", "Global", 8, 
                          ["Frederick the Great", "Maria Theresa"]),
            HistoricalEvent("American Revolution Begins", 1775, "Political", "North America", 9, 
                          ["George Washington", "King George III"]),
            HistoricalEvent("French Revolution Begins", 1789, "Political", "France", 10, 
                          ["Third Estate", "Louis XVI"])
        ]
        
        self.events = sample_events
        print(f"Loaded {len(self.events)} historical events for analysis")
    
    def analyze_by_century(self):
        """Analyze events by century and identify patterns"""
        print("\nCentury-by-Century Analysis:")
        print("=" * 50)
        
        centuries = {}
        for event in self.events:
            century = (event.year // 100) + 1
            if century not in centuries:
                centuries[century] = []
            centuries[century].append(event)
        
        for century in sorted(centuries.keys()):
            events = centuries[century]
            print(f"\n{century}th Century ({len(events)} events):")
            print("-" * 30)
            
            # Analyze event types
            event_types = {}
            total_significance = 0
            
            for event in events:
                event_type = event.event_type
                event_types[event_type] = event_types.get(event_type, 0) + 1
                total_significance += event.significance
            
            # Display events
            for event in sorted(events, key=lambda x: x.year):
                print(f"  {event.year}: {event.name} (Significance: {event.significance}/10)")
            
            # Century statistics
            avg_significance = total_significance / len(events)
            print(f"\n  Century Statistics:")
            print(f"  • Average significance: {avg_significance:.1f}/10")
            print(f"  • Event types: {dict(event_types)}")
            print(f"  • Most common type: {max(event_types, key=event_types.get)}")
    
    def analyze_event_clustering(self):
        """Find clusters of events that happened close together in time"""
        print("\nEvent Clustering Analysis:")
        print("=" * 40)
        
        # Sort events by year
        sorted_events = sorted(self.events, key=lambda x: x.year)
        
        clusters = []
        current_cluster = [sorted_events[0]]
        
        for i in range(1, len(sorted_events)):
            current_event = sorted_events[i]
            last_event = current_cluster[-1]
            
            # If events are within 50 years, add to current cluster
            if current_event.year - last_event.year <= 50:
                current_cluster.append(current_event)
            else:
                # Start new cluster if current one has multiple events
                if len(current_cluster) > 1:
                    clusters.append(current_cluster)
                current_cluster = [current_event]
        
        # Don't forget the last cluster
        if len(current_cluster) > 1:
            clusters.append(current_cluster)
        
        print(f"Found {len(clusters)} event clusters (events within 50 years):")
        
        for i, cluster in enumerate(clusters, 1):
            start_year = min(event.year for event in cluster)
            end_year = max(event.year for event in cluster)
            
            print(f"\nCluster {i}: {start_year}-{end_year} ({len(cluster)} events)")
            print("-" * 30)
            
            for event in cluster:
                print(f"  • {event.year}: {event.name}")
            
            # Analyze cluster characteristics
            types = {}
            locations = {}
            for event in cluster:
                types[event.event_type] = types.get(event.event_type, 0) + 1
                locations[event.location] = locations.get(event.location, 0) + 1
            
            print(f"  Dominant type: {max(types, key=types.get)}")
            print(f"  Primary locations: {', '.join(list(locations.keys())[:3])}")
    
    def analyze_historical_impact(self):
        """Analyze events by their historical significance and impact"""
        print("\nHistorical Impact Analysis:")
        print("=" * 40)
        
        # Sort by significance
        by_significance = sorted(self.events, key=lambda x: x.significance, reverse=True)
        
        print("Top 10 Most Significant Events:")
        print("-" * 35)
        for i, event in enumerate(by_significance[:10], 1):
            print(f"{i:2d}. {event.name} ({event.year}) - Impact: {event.significance}/10")
            print(f"     Type: {event.event_type}, Location: {event.location}")
        
        # Analyze by event type
        print(f"\nSignificance by Event Type:")
        print("-" * 30)
        
        type_analysis = {}
        for event in self.events:
            event_type = event.event_type
            if event_type not in type_analysis:
                type_analysis[event_type] = {'total': 0, 'count': 0, 'events': []}
            
            type_analysis[event_type]['total'] += event.significance
            type_analysis[event_type]['count'] += 1
            type_analysis[event_type]['events'].append(event)
        
        for event_type, data in sorted(type_analysis.items(), 
                                     key=lambda x: x[1]['total']/x[1]['count'], reverse=True):
            avg_significance = data['total'] / data['count']
            print(f"• {event_type}: {avg_significance:.1f} avg significance ({data['count']} events)")
    
    def find_historical_patterns(self):
        """Identify patterns and trends in historical data"""
        print("\nHistorical Pattern Analysis:")
        print("=" * 40)
        
        # Analyze frequency of event types over time
        early_period = [e for e in self.events if e.year < 1000]
        middle_period = [e for e in self.events if 1000 <= e.year < 1500]
        late_period = [e for e in self.events if e.year >= 1500]
        
        periods = [
            ("Early Period (pre-1000)", early_period),
            ("Middle Period (1000-1499)", middle_period),
            ("Late Period (1500+)", late_period)
        ]
        
        for period_name, period_events in periods:
            if not period_events:
                continue
                
            print(f"\n{period_name}: {len(period_events)} events")
            print("-" * 40)
            
            # Count event types
            type_counts = {}
            for event in period_events:
                type_counts[event.event_type] = type_counts.get(event.event_type, 0) + 1
            
            # Calculate percentages
            total = len(period_events)
            for event_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total) * 100
                print(f"  • {event_type}: {count} events ({percentage:.1f}%)")
    
    def export_timeline_data(self, filename="historical_analysis.json"):
        """Export analysis results to JSON file"""
        print(f"\nExporting timeline data to {filename}...")
        
        export_data = {
            'metadata': {
                'total_events': len(self.events),
                'time_span': f"{min(e.year for e in self.events)}-{max(e.year for e in self.events)}",
                'analysis_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            'events': [event.to_dict() for event in self.events],
            'statistics': self.calculate_statistics()
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(export_data, file, indent=2, ensure_ascii=False)
            print(f"Successfully exported {len(self.events)} events to {filename}")
        except Exception as e:
            print(f"Error exporting data: {e}")
    
    def calculate_statistics(self):
        """Calculate comprehensive statistics for export"""
        stats = {}
        
        # Basic statistics
        years = [e.year for e in self.events]
        stats['time_range'] = {'start': min(years), 'end': max(years)}
        stats['total_span_years'] = max(years) - min(years)
        
        # Event type distribution
        type_counts = {}
        significance_by_type = {}
        
        for event in self.events:
            event_type = event.event_type
            type_counts[event_type] = type_counts.get(event_type, 0) + 1
            
            if event_type not in significance_by_type:
                significance_by_type[event_type] = []
            significance_by_type[event_type].append(event.significance)
        
        stats['event_types'] = type_counts
        stats['average_significance_by_type'] = {
            event_type: sum(sigs)/len(sigs) 
            for event_type, sigs in significance_by_type.items()
        }
        
        # Overall significance statistics
        all_significance = [e.significance for e in self.events]
        stats['significance'] = {
            'average': sum(all_significance) / len(all_significance),
            'minimum': min(all_significance),
            'maximum': max(all_significance)
        }
        
        return stats
    
    def interactive_query_system(self):
        """Interactive system for querying historical data"""
        print("\nInteractive Historical Query System")
        print("=" * 40)
        print("Available commands:")
        print("1. 'year YYYY' - Find events in specific year")
        print("2. 'type EVENT_TYPE' - Find events of specific type")
        print("3. 'location PLACE' - Find events in specific location")
        print("4. 'significance N' - Find events with significance >= N")
        print("5. 'participant NAME' - Find events involving specific person")
        print("6. 'between YYYY YYYY' - Find events between two years")
        print("7. 'quit' - Exit query system")
        
        while True:
            query = input("\nEnter query (or 'quit' to exit): ").strip().lower()
            
            if query == 'quit':
                print("Exiting query system...")
                break
            
            try:
                parts = query.split()
                command = parts[0]
                
                if command == 'year' and len(parts) == 2:
                    year = int(parts[1])
                    results = [e for e in self.events if e.year == year]
                    self.display_query_results(f"Events in {year}", results)
                
                elif command == 'type' and len(parts) >= 2:
                    event_type = ' '.join(parts[1:]).title()
                    results = [e for e in self.events if e.event_type.lower() == event_type.lower()]
                    self.display_query_results(f"{event_type} events", results)
                
                elif command == 'location' and len(parts) >= 2:
                    location = ' '.join(parts[1:]).title()
                    results = [e for e in self.events if location.lower() in e.location.lower()]
                    self.display_query_results(f"Events in {location}", results)
                
                elif command == 'significance' and len(parts) == 2:
                    min_sig = int(parts[1])
                    results = [e for e in self.events if e.significance >= min_sig]
                    self.display_query_results(f"Events with significance >= {min_sig}", results)
                
                elif command == 'participant' and len(parts) >= 2:
                    name = ' '.join(parts[1:]).title()
                    results = []
                    for event in self.events:
                        for participant in event.participants:
                            if name.lower() in participant.lower():
                                results.append(event)
                                break
                    self.display_query_results(f"Events involving {name}", results)
                
                elif command == 'between' and len(parts) == 3:
                    start_year = int(parts[1])
                    end_year = int(parts[2])
                    results = [e for e in self.events if start_year <= e.year <= end_year]
                    self.display_query_results(f"Events between {start_year}-{end_year}", results)
                
                else:
                    print("Invalid query format. Please try again.")
                    
            except (ValueError, IndexError):
                print("Error parsing query. Please check the format and try again.")
    
    def display_query_results(self, title, results):
        """Display formatted query results"""
        print(f"\n{title}:")
        print("-" * len(title))
        
        if not results:
            print("No events found matching your criteria.")
            return
        
        # Sort results by year
        sorted_results = sorted(results, key=lambda x: x.year)
        
        for event in sorted_results:
            print(f"• {event.year}: {event.name}")
            print(f"  Type: {event.event_type}, Location: {event.location}")
            print(f"  Significance: {event.significance}/10")
            if event.participants:
                print(f"  Key figures: {', '.join(event.participants[:3])}")
        
        print(f"\nFound {len(results)} matching events.")
    
    def comprehensive_analysis_report(self):
        """Generate a complete analysis report combining all methods"""
        print("\n" + "=" * 80)
        print("COMPREHENSIVE HISTORICAL TIMELINE ANALYSIS REPORT")
        print("=" * 80)
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Dataset: {len(self.events)} historical events")
        print(f"Time Period: {min(e.year for e in self.events)}-{max(e.year for e in self.events)} CE")
        
        # Run all analysis methods
        self.analyze_by_century()
        self.analyze_event_clustering()
        self.analyze_historical_impact()
        self.find_historical_patterns()
        
        # Export data
        self.export_timeline_data()
        
        print("\n" + "=" * 80)
        print("REPORT SUMMARY")
        print("=" * 80)
        
        # Generate summary statistics
        total_events = len(self.events)
        event_types = set(e.event_type for e in self.events)
        locations = set(e.location for e in self.events)
        avg_significance = sum(e.significance for e in self.events) / total_events
        
        print(f"• Total Events Analyzed: {total_events}")
        print(f"• Event Types: {len(event_types)} ({', '.join(sorted(event_types))})")
        print(f"• Geographic Coverage: {len(locations)} locations")
        print(f"• Average Historical Significance: {avg_significance:.1f}/10")
        
        # Most significant events
        top_events = sorted(self.events, key=lambda x: x.significance, reverse=True)[:5]
        print(f"\nTop 5 Most Significant Events:")
        for i, event in enumerate(top_events, 1):
            print(f"  {i}. {event.name} ({event.year}) - {event.significance}/10")

# Main execution with menu system
def main():
    """Main function with interactive menu"""
    analyzer = HistoricalTimelineAnalyzer()
    
    while True:
        print("\n" + "=" * 60)
        print("HISTORICAL TIMELINE ANALYSIS SYSTEM")
        print("=" * 60)
        print("1. Run Comprehensive Analysis Report")
        print("2. Analyze by Century")
        print("3. Find Event Clusters")
        print("4. Analyze Historical Impact")
        print("5. Find Historical Patterns")
        print("6. Interactive Query System")
        print("7. Export Data to JSON")
        print("8. Exit")
        
        try:
            choice = input("\nSelect an option (1-8): ").strip()
            
            if choice == '1':
                analyzer.comprehensive_analysis_report()
            elif choice == '2':
                analyzer.analyze_by_century()
            elif choice == '3':
                analyzer.analyze_event_clustering()
            elif choice == '4':
                analyzer.analyze_historical_impact()
            elif choice == '5':
                analyzer.find_historical_patterns()
            elif choice == '6':
                analyzer.interactive_query_system()
            elif choice == '7':
                analyzer.export_timeline_data()
            elif choice == '8':
                print("Thank you for using the Historical Timeline Analysis System!")
                break
            else:
                print("Invalid choice. Please enter a number between 1-8.")
                
        except KeyboardInterrupt:
            print("\n\nExiting program...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()