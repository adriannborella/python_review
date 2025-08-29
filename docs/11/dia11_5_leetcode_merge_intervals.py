"""
LeetCode 56: Merge Intervals (MEDIUM)
Problema EXTREMADAMENTE COMÚN en entrevistas

Given: [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]

Key insight: Sorting + greedy merging
"""

def merge_intervals(intervals):
    """
    Standard merge intervals solution
    
    Time: O(n log n) due to sorting
    Space: O(1) excluding output
    """
    if not intervals:
        return []
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        last_merged = merged[-1]
        
        # Check if current interval overlaps with last merged
        if current[0] <= last_merged[1]:
            # Merge: extend the end time
            last_merged[1] = max(last_merged[1], current[1])
        else:
            # No overlap: add as new interval
            merged.append(current)
    
    return merged

def insert_interval(intervals, new_interval):
    """
    LeetCode 57: Insert Interval
    Given sorted intervals, insert new interval and merge
    
    More complex: need to handle insertion position
    """
    result = []
    i = 0
    n = len(intervals)
    
    # Add all intervals that end before new interval starts
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1
    
    # Merge overlapping intervals with new interval
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    
    result.append(new_interval)
    
    # Add remaining intervals
    while i < n:
        result.append(intervals[i])
        i += 1
    
    return result

def can_attend_meetings(intervals):
    """
    LeetCode 252: Meeting Rooms
    Determine if person can attend all meetings
    
    Simpler variation - just check for overlaps
    """
    if not intervals:
        return True
    
    intervals.sort(key=lambda x: x[0])
    
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False
    
    return True

def min_meeting_rooms(intervals):
    """
    LeetCode 253: Meeting Rooms II
    Find minimum number of meeting rooms required
    
    Advanced: Uses event processing technique
    """
    if not intervals:
        return 0
    
    # Create events: +1 for start, -1 for end
    events = []
    for start, end in intervals:
        events.append((start, 1))    # Meeting starts
        events.append((end, -1))     # Meeting ends
    
    # Sort events by time, prioritize end events when tied
    events.sort(key=lambda x: (x[0], x[1]))
    
    concurrent_meetings = 0
    max_rooms = 0
    
    for time, event_type in events:
        concurrent_meetings += event_type
        max_rooms = max(max_rooms, concurrent_meetings)
    
    return max_rooms

def min_meeting_rooms_heap(intervals):
    """
    Alternative solution using heap (more intuitive)
    """
    import heapq
    
    if not intervals:
        return 0
    
    intervals.sort(key=lambda x: x[0])
    
    # Min heap to track end times of ongoing meetings
    heap = []
    
    for start, end in intervals:
        # Remove meetings that have ended
        while heap and heap[0] <= start:
            heapq.heappop(heap)
        
        # Add current meeting's end time
        heapq.heappush(heap, end)
    
    return len(heap)

def erase_overlap_intervals(intervals):
    """
    LeetCode 435: Non-overlapping Intervals
    Find minimum number of intervals to remove
    
    Greedy approach: always keep interval with earliest end time
    """
    if not intervals:
        return 0
    
    intervals.sort(key=lambda x: x[1])  # Sort by end time
    
    count = 0
    end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        if intervals[i][0] < end:
            # Overlapping interval - need to remove one
            count += 1
        else:
            # No overlap - update end time
            end = intervals[i][1]
    
    return count

def interval_intersection(firstList, secondList):
    """
    LeetCode 986: Interval List Intersections
    Find intersection of two sorted interval lists
    
    Two-pointer technique
    """
    result = []
    i = j = 0
    
    while i < len(firstList) and j < len(secondList):
        # Find intersection
        start = max(firstList[i][0], secondList[j][0])
        end = min(firstList[i][1], secondList[j][1])
        
        # If valid intersection exists
        if start <= end:
            result.append([start, end])
        
        # Move pointer of interval that ends first
        if firstList[i][1] < secondList[j][1]:
            i += 1
        else:
            j += 1
    
    return result

# COMPREHENSIVE TESTING
def test_interval_problems():
    """
    Testing all interval problems - typical interview scenarios
    """
    
    # Test merge intervals
    intervals1 = [[1,3],[2,6],[8,10],[15,18]]
    expected1 = [[1,6],[8,10],[15,18]]
    assert merge_intervals(intervals1) == expected1
    
    # Edge cases for merge
    assert merge_intervals([]) == []
    assert merge_intervals([[1,4]]) == [[1,4]]
    assert merge_intervals([[1,4],[4,5]]) == [[1,5]]  # Adjacent intervals
    
    print("✅ Merge Intervals tests passed")
    
    # Test insert interval
    intervals2 = [[1,3],[6,9]]
    new_interval2 = [2,5]
    expected2 = [[1,5],[6,9]]
    assert insert_interval(intervals2, new_interval2) == expected2
    
    intervals3 = [[1,2],[3,5],[6,7],[8,10],[12,16]]
    new_interval3 = [4,8]
    expected3 = [[1,2],[3,10],[12,16]]
    assert insert_interval(intervals3, new_interval3) == expected3
    
    print("✅ Insert Interval tests passed")
    
    # Test meeting rooms
    meetings1 = [[0,30],[5,10],[15,20]]
    assert can_attend_meetings(meetings1) == False
    
    meetings2 = [[7,10],[2,4]]
    assert can_attend_meetings(meetings2) == True
    
    print("✅ Meeting Rooms I tests passed")
    
    # Test meeting rooms II
    meetings3 = [[0,30],[5,10],[15,20]]
    assert min_meeting_rooms(meetings3) == 2
    assert min_meeting_rooms_heap(meetings3) == 2
    
    meetings4 = [[7,10],[2,4]]
    assert min_meeting_rooms(meetings4) == 1
    assert min_meeting_rooms_heap(meetings4) == 1
    
    print("✅ Meeting Rooms II tests passed")
    
    # Test erase overlap intervals
    intervals4 = [[1,2],[2,3],[3,4],[1,3]]
    assert erase_overlap_intervals(intervals4) == 1
    
    intervals5 = [[1,2],[1,2],[1,2]]
    assert erase_overlap_intervals(intervals5) == 2
    
    print("✅ Erase Overlap Intervals tests passed")
    
    # Test interval intersection
    firstList = [[0,2],[5,10],[13,23],[24,25]]
    secondList = [[1,5],[8,12],[15,24],[25,26]]
    expected_intersection = [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]
    assert interval_intersection(firstList, secondList) == expected_intersection
    
    print("✅ Interval Intersection tests passed")

# INTERVIEW TIPS Y PATTERNS
def interview_patterns_intervals():
    """
    Patterns comunes para problemas de intervals:
    
    1. SORTING: Casi siempre necesitas sort by start time
    2. GREEDY: Para merge/remove, greedy approach often works
    3. TWO POINTERS: Para intersections entre dos listas
    4. HEAP: Para tracking multiple ongoing events (meeting rooms)
    5. EVENT PROCESSING: Para problems con múltiples start/end times
    
    Common gotchas:
    - Edge case: empty intervals
    - Boundary case: [1,2] y [2,3] se consideran non-overlapping
    - Always check if intervals are pre-sorted
    """
    pass

if __name__ == "__main__":
    test_interval_problems()
    
    print("\n🎯 INTERVIEW TIPS:")
    print("1. Always ask: Are intervals pre-sorted?")
    print("2. Clarify: Do [1,2] and [2,3] overlap? (Usually no)")
    print("3. Consider: What if intervals array is empty?")
    print("4. Time complexity: Usually O(n log n) due to sorting")
    print("5. Space complexity: Usually O(1) excluding output")