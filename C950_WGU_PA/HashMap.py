# Class for implementing custom hash map.

# SUMMARIZED SOURCE: This hashmap was loosely based on WGU course webinar material.
# WGU code repository W-2_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy.py
class CreateHashMap:
    def __init__(self, capacity=20):
        self.list = []
        for i in range(capacity):  # O(n) complexity as it is going to iterate through 'n' items in the list.
            self.list.append([])

    # This method allows insertion into the hash map. bucket_list will hold the given item.
    def insert(self, key, item):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        for kv in bucket_list:  # O(n) complexity as it is going to iterate through 'n' items in the list.
            if kv[0] == key:
                kv[1] = item
                return True

        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # This method allows searching in the hash map with linear probing. bucket_list will hold the given item.
    def search(self, key):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]
        for pair in bucket_list:  # O(n) complexity as it is going to iterate through 'n' items in the list.
            if key == pair[0]:
                return pair[1]
        return None

    # Method for removing selected item from the table.
    # Complexity of O(1) as it is a constant operation.
    def remove(self, key):
        slot = hash(key) % len(self.list)
        destination = self.list[slot]

        if key in destination:
            destination.remove(key)
