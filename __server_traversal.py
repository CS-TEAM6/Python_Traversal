
import requests
import time

api = "https://lambda-treasure-hunt.herokuapp.com/api/adv"


current_room = 999
previous_room = 999
cooldown = 15

traversalPath = []

visited = {}

path = []

# add starting room to visited
r = requests.get(url=api + "/init", headers = {"Authorization": "Token"})

data = r.json()

data["room_exits"] = {"n":"?", "s":"?", "e":"?", "w":"?"}
visited[data["room_id"]] = data

current_room = data["room_id"]
print("Current room:", current_room)



def go(direction):

    print(f"Go: {direction}")

    direction_inverse = {"s": "n", "n": "s", "w": "e", "e": "w"}
    prev_direction = direction_inverse[direction]

    global current_room
    global previous_room
    global cooldown
    global data
    
    time.sleep(cooldown)

    previous_room = current_room

    post_data = {"direction": direction}

    if visited[previous_room]["room_exits"][direction] is not "?":
        post_data = {"direction": direction, "next_room_id": f"{visited[previous_room]['room_exits'][direction]}"}
        print("Wise Explorer")
        print(visited[previous_room]["room_exits"][direction])

    r = requests.post(url=api + "/move", json=post_data, headers = {"Authorization": "Token"})

    data = r.json()

    if "room_exits" not in data:
        data["room_exits"] = {"n":"?", "s":"?", "e":"?", "w":"?"}

        
    data["room_exits"][prev_direction] = previous_room


    current_room = data["room_id"]
    cooldown = data["cooldown"]


    visited[previous_room]["room_exits"][direction] = current_room

    
    print(f"Previous room: {previous_room} . Direction: {prev_direction}")
    print("Current room:", current_room)
    print(f"Cooldown: {cooldown}")



while len(visited) < 500:
    if current_room not in visited:
        visited[data["room_id"]] = data

        f= open("test.txt","w")
        f.write(f"Number of rooms visited: {len(visited)}\n\n{visited}")
        f.close()


        
        previous_direction = path[-1]
        visited[current_room]["exits"].remove(previous_direction)
        print(f"\nVISITED ROOMS: {len(visited)}")
        print(f"Path Length: {len(path)}")


    while len(visited[current_room]["exits"]) < 1:
        previous_direction = path.pop()
        traversalPath.append(previous_direction)        
        
        f= open("test.txt","w")
        f.write(f"Number of rooms visited: {len(visited)}\n\n{visited}")
        f.close()

        go(previous_direction)

        
    direction_inverse = {"s": "n", "n": "s", "w": "e", "e": "w"}
    move = visited[current_room]["exits"].pop(0)
    traversalPath.append(move)
    path.append(direction_inverse[move])    
        
    f= open("test.txt","w")
    f.write(f"Number of rooms visited: {len(visited)}\n\n{visited}")
    f.close()

    go(move)

        
f= open("test.txt","w")
f.write(f"Number of rooms visited: {len(visited)}\n\n{visited}")
f.close()


print("visited:", visited)