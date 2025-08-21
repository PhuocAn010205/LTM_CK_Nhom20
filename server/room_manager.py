class RoomManager:
    def __init__(self):
        self.rooms = {}

    def add_user_to_room(self, user_addr, room):
        if room not in self.rooms:
            self.rooms[room] = set()
        self.rooms[room].add(user_addr)
        return True

    def remove_user_from_room(self, user_addr, room):
        if room in self.rooms and user_addr in self.rooms[room]:
            self.rooms[room].remove(user_addr)
            return True
        return False

    def is_user_in_room(self, user_addr, room):
        return room in self.rooms and user_addr in self.rooms[room]

    def is_room_active(self, room):
        return room in self.rooms and len(self.rooms[room]) > 0

    def close_room(self, room):
        if room in self.rooms:
            del self.rooms[room]


room_manager = RoomManager()
