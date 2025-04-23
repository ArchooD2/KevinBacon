# Standard library imports
import os
import time
import json
import snaparg as argparse
from collections import deque
from concurrent.futures import ThreadPoolExecutor

# Third-party library imports
import wikipediaapi

current_dir = os.path.dirname(__file__)  # Directory of baconwaffle.py
json_file_path = os.path.join(current_dir, "json_cache", "cache.json")


def args():
    parser = argparse.ArgumentParser(
        description="Find the shortest path between two Wikipedia articles."
    )
    parser.add_argument(
        "--source", "-s", type=str, required=True, help="Source Article"
    )
    parser.add_argument("--target", "-t", type=str, help="Destination Article")
    parser.add_argument("--depth", "-d", type=int, help="Depth Maximum")
    args = parser.parse_args()

    return args.source, args.target, args.depth


def find_shortest_path(start_title, end_title=None, max_depth=None):
    if end_title is None:
        end_title = "Kevin Bacon"
    if max_depth is None:
        max_depth = 7
    cached_flag = check_or_save(start_title.lower(), end_title.lower())
    if cached_flag:
        print(f"Found path from {start_title} to {end_title}")
        return

    # Initialize Wikipedia API
    user_agent = "KevinBaconScript/1.0 (archood2next@gmail.com)bot"
    wiki = wikipediaapi.Wikipedia(user_agent)

    def get_links(title):
        page = wiki.page(title)
        print(f"Getting links of {title}")
        if page.exists():
            links = [
                (
                    link.title
                    if link.namespace == wikipediaapi.Namespace.MAIN
                    else link.text
                )
                for link in page.links.values()
                if not any(
                    link.title.startswith(prefix) or keyword in link.title.lower()
                    for prefix in [
                        "Category:",
                        "Help:",
                        "Wikipedia:",
                        "Template:",
                        "Template talk:",
                        "Portal:",
                        "List",
                        "User:",
                        "Main Page",
                        "User talk:",
                        "Talk:",
                        "Wikipedia",
                        "Draft",
                    ]
                    for keyword in ["election", "conference"]
                )
            ]
            # Include redirects
            for section in page.sections:
                if section.title == "Redirects":
                    links.extend(section.links.keys())
            return links
        return []

    def get_backlinks(title):
        page = wiki.page(title)
        print(f"Getting backlinks of {title}")
        if page.exists():
            # print(f"Backlinks count: {len(page.backlinks)}")  # Debugging output
            links = [
                link.title
                for link in page.backlinks.values()
                if not any(
                    link.title.startswith(prefix) or keyword in link.title.lower()
                    for prefix in [
                        "Category:",
                        "Help:",
                        "Wikipedia:",
                        "Template:",
                        "Template talk:",
                        "Portal:",
                        "List",
                        "User:",
                        "Main Page",
                        "User talk:",
                        "Talk:",
                        "Wikipedia",
                        "Draft",
                    ]
                    for keyword in ["election", "conference"]
                )
            ]
            # print(f"Filtered backlinks: {links}")  # Debugging output
            return links
        return []

    def bidirectional_bfs(start, end, max_depth):
        forward_queue = deque([(start, [start])])
        backward_queue = deque([(end, [end])])
        forward_visited = {start: [start]}
        backward_visited = {end: [end]}
        forward_cached_links = {}
        backward_cached_links = {}

        while forward_queue and backward_queue:
            # Forward BFS
            if forward_queue:
                current, path = forward_queue.popleft()
                if current in backward_visited:
                    if is_valid_path(
                        start_title,
                        end_title,
                        path + backward_visited[current][::-1][1:],
                    ):
                        return path + backward_visited[current][::-1][1:]
                if len(path) <= max_depth:
                    if current not in forward_cached_links:
                        forward_cached_links[current] = get_links(current)
                    links_to_fetch = [
                        link
                        for link in forward_cached_links[current]
                        if link not in forward_visited and link
                    ]
                    with ThreadPoolExecutor(max_workers=16) as executor:
                        futures = [
                            executor.submit(lambda x: (x, path + [x]), link)
                            for link in links_to_fetch
                        ]
                        for future in futures:
                            result = future.result()
                            if result[0] not in forward_visited:
                                forward_queue.append(result)
                                forward_visited[result[0]] = result[1]

            # Backward BFS
            if backward_queue:
                current, path = backward_queue.popleft()
                if current in forward_visited:
                    if is_valid_path(
                        start_title,
                        end_title,
                        forward_visited[current] + path[::-1][1:],
                    ):
                        return forward_visited[current] + path[::-1][1:]
                if len(path) <= max_depth:
                    if current not in backward_cached_links:
                        backward_cached_links[current] = get_backlinks(current)
                    links_to_fetch = [
                        link
                        for link in backward_cached_links[current]
                        if link not in backward_visited and link
                    ]
                    with ThreadPoolExecutor(max_workers=16) as executor:
                        futures = [
                            executor.submit(lambda x: (x, path + [x]), link)
                            for link in links_to_fetch
                        ]
                        for future in futures:
                            result = future.result()
                            if result[0] not in backward_visited:
                                backward_queue.append(result)
                                backward_visited[result[0]] = result[1]

        return None

    def is_valid_path(start, end, path):
        print("=====================================")
        print(f"Checking Path: {path}")

        # Check if the path is valid from start to end via Wikipedia API
        current = start
        path.pop(0)
        if "" in path or "" in path:
            # something fucked up, figure out what threw us a blank-ass bone.
            empty_article = path.index("" if "" in path else "")
            print(f"Empty string found in article: {path[empty_article]}")
            print("=====================================")
        for step in path:
            print(f"checking for:{step} in {current}")
            if current == end:
                print("Yep!")
                print("=====================================")
                return True
            if step in get_links(current):
                current = step
            else:
                print("Nope!")
                print("=====================================")
                return False

        return current == end

    start_time = time.time()
    path = bidirectional_bfs(start_title, end_title, max_depth)
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")
    if path:
        print(f"Found a path from '{start_title}' to '{end_title}':")
        print_path(path)
        check_or_save(start_title.lower(), end_title.lower(), save=True)
        return path
    else:
        print(
            f"No path found from '{start_title}' to '{end_title}' within depth {max_depth}."
        )


def check_or_save(start_title, end_title, save=False) -> bool:
    with open(json_file_path, mode="r", encoding="utf-8") as _fp:
        saved_path_file = json.load(_fp) or {}
    if save:
        saved_path_file.update({f"{start_title}-{end_title}": "yes"})
        print("Saving this path in file, for faster access")
        with open(json_file_path, "w") as _fp:
            json.dump(saved_path_file, _fp)
    else:
        _check = saved_path_file.get(f"{start_title}-{end_title}")
        if not _check:
            print("Not saved in cache memory, running wikipedia query")
            return False
        return True


def print_path(path):
    for i, step in enumerate(path):
        print(f"Step {i+1}: {step}")


if __name__ == "__main__":
    start_article, end_article, depth = args()
    find_shortest_path(start_article, end_article, depth)
