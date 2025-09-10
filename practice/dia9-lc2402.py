from typing import List
import heapq
from utils import values_meetings


class Solution:
    def mostBooked(self, n: int, meetings: List[List[int]]) -> int:
        """
        LeetCode 2402: Meeting rooms 3

        You are given an integer n. There are n rooms numbered from 0 to n - 1.

        You are given a 2D integer array meetings where meetings[i] = [starti, endi] means that a meeting will be held during the half-closed time interval [starti, endi). All the values of starti are unique.

        Meetings are allocated to rooms in the following manner:

        Each meeting will take place in the unused room with the lowest number.
        If there are no available rooms, the meeting will be delayed until a room becomes free. The delayed meeting should have the same duration as the original meeting.
        When a room becomes unused, meetings that have an earlier original start time should be given the room.
        Return the number of the room that held the most meetings. If there are multiple rooms, return the room with the lowest number.

        A half-closed interval [a, b) is the interval between a and b including a and not including b.
        """
        meetings.sort(key=lambda x: x[0])
        rooms = {r: {"meeting_count": 0} for r in range(n)}

        free_roms = list(range(n))
        busy_rooms = []
        result = 0
        max_meetings = 0

        for start_time, end_time in meetings:

            # clean finished rooms
            while busy_rooms and busy_rooms[0][0] <= start_time:
                _, r_number = heapq.heappop(busy_rooms)
                heapq.heappush(free_roms, r_number)

            if free_roms:
                room_number = heapq.heappop(free_roms)
                new_end = end_time
            else:
                old_end, room_number = heapq.heappop(busy_rooms)
                new_end = old_end + (end_time - start_time)

            heapq.heappush(busy_rooms, (new_end, room_number))
            rooms[room_number]["meeting_count"] += 1

            if rooms[room_number]["meeting_count"] > max_meetings or (
                rooms[room_number]["meeting_count"] == max_meetings
                and room_number < result
            ):
                result = room_number
                max_meetings = rooms[room_number]["meeting_count"]

        return result


sol = Solution()
assert sol.mostBooked(2, [[0, 10], [1, 5], [2, 7], [3, 4]]) == 0, "Test case 1"
assert sol.mostBooked(3, [[1, 20], [2, 10], [3, 5], [4, 9], [6, 8]]) == 1, "Test case 2"
assert sol.mostBooked(3, [[13, 16], [12, 19]]) == 0, "Test case 3"
assert sol.mostBooked(100, values_meetings) == 15, "Test case 4"
assert (
    sol.mostBooked(4, [[18, 19], [3, 12], [17, 19], [2, 13], [7, 10]]) == 0
), "Test case 5"
