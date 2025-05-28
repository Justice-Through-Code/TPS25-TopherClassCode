# Advanced Example 1: Text Processing Optimization
# This builds on the basic examples to create a real text processing program

import time
import string

class TextProcessor:
    """A class that processes text files efficiently using optimization techniques"""
    
    def __init__(self):
        # Pre-calculate things we'll use often (seed improvement!)
        self.word_count_cache = {}
        self.punctuation_set = set(string.punctuation)  # Set for fast lookup
        
    def clean_text_slow(self, text):
        """Slow version - shows what NOT to do"""
        # Bad: Creating new strings repeatedly
        result = ""
        for char in text.lower():
            if char not in string.punctuation:  # Slow: searches list every time
                result += char  # Slow: string concatenation
            else:
                result += " "
        return result
    
    def clean_text_fast(self, text):
        """Fast version - applies our optimization techniques"""
        # Good: Use list comprehension and pre-calculated set
        chars = [char if char not in self.punctuation_set else ' ' 
                for char in text.lower()]
        return ''.join(chars)  # Fast: join method
    
    def count_words_slow(self, text):
        """Slow word counting"""
        words = text.split()
        word_counts = {}
        
        # Bad: Using list.count() which searches the whole list each time
        unique_words = list(set(words))
        for word in unique_words:
            word_counts[word] = words.count(word)  # This is very slow!
        
        return word_counts
    
    def count_words_fast(self, text):
        """Fast word counting with caching"""
        # Check if we've already processed this text
        text_id = hash(text)
        if text_id in self.word_count_cache:
            return self.word_count_cache[text_id]
        
        # Good: Count as we go, using get() method
        words = text.split()
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        # Cache the result for next time
        self.word_count_cache[text_id] = word_counts
        return word_counts
    
    def find_common_words_slow(self, word_counts, min_count=5):
        """Slow way to find common words"""
        common_words = []
        for word in word_counts:
            if word_counts[word] >= min_count:
                common_words.append(word)
        return common_words
    
    def find_common_words_fast(self, word_counts, min_count=5):
        """Fast way using list comprehension"""
        return [word for word, count in word_counts.items() if count >= min_count]
    
    def analyze_text(self, text, use_fast_methods=True):
        """Complete text analysis using fast or slow methods"""
        results = {}
        
        if use_fast_methods:
            print("Using optimized methods...")
            
            # Clean text (fast)
            start_time = time.time()
            clean_text = self.clean_text_fast(text)
            clean_time = time.time() - start_time
            
            # Count words (fast)
            start_time = time.time()
            word_counts = self.count_words_fast(clean_text)
            count_time = time.time() - start_time
            
            # Find common words (fast)
            start_time = time.time()
            common_words = self.find_common_words_fast(word_counts)
            common_time = time.time() - start_time
            
        else:
            print("Using slow methods...")
            
            # Clean text (slow)
            start_time = time.time()
            clean_text = self.clean_text_slow(text)
            clean_time = time.time() - start_time
            
            # Count words (slow)
            start_time = time.time()
            word_counts = self.count_words_slow(clean_text)
            count_time = time.time() - start_time
            
            # Find common words (slow)
            start_time = time.time()
            common_words = self.find_common_words_slow(word_counts)
            common_time = time.time() - start_time
        
        results = {
            'total_words': len(clean_text.split()),
            'unique_words': len(word_counts),
            'common_words': len(common_words),
            'times': {
                'cleaning': clean_time,
                'counting': count_time,
                'finding_common': common_time,
                'total': clean_time + count_time + common_time
            }
        }
        
        return results

# Demo the text processor
if __name__ == "__main__":
    # Sample text (in real life, this might come from a file)
    sample_text = """
    Python is a great programming language. Python is easy to learn.
    Many people love Python because Python is readable and Python is powerful.
    Learning Python takes time, but Python rewards patience. Python, Python, Python!
    The Python community is welcoming. Python developers are helpful.
    """ * 100  # Repeat to make it bigger for timing
    
    processor = TextProcessor()
    
    print("=== Text Processing Performance Comparison ===")
    print(f"Text length: {len(sample_text)} characters")
    
    # Test slow methods
    print("\n--- Slow Methods ---")
    slow_results = processor.analyze_text(sample_text, use_fast_methods=False)
    
    # Test fast methods
    print("\n--- Fast Methods ---")
    fast_results = processor.analyze_text(sample_text, use_fast_methods=True)
    
    # Show results
    print(f"\n=== Results ===")
    print(f"Total words: {fast_results['total_words']}")
    print(f"Unique words: {fast_results['unique_words']}")
    print(f"Common words (5+ occurrences): {fast_results['common_words']}")
    
    print(f"\n=== Performance Comparison ===")
    slow_total = slow_results['times']['total']
    fast_total = fast_results['times']['total']
    
    print(f"Slow methods total: {slow_total:.4f} seconds")
    print(f"Fast methods total: {fast_total:.4f} seconds")
    print(f"Speed improvement: {slow_total/fast_total:.2f}x faster")
    
    print(f"\n🎯 Key Takeaway: Combining multiple optimizations creates dramatic improvements!")