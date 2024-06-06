import wikipediaapi
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import time

def find_shortest_path(start_title, end_title="Kevin Bacon", max_depth=7):
    # Initialize Wikipedia API
    user_agent = "KevinBaconScript/1.0 (archood2next@gmail.com)bot"
    wiki = wikipediaapi.Wikipedia(user_agent)
    
    def get_links(title):
        page = wiki.page(title)
        if page.exists():
            links = [link for link in page.links.keys() if not any(
                link.startswith(prefix) or keyword in link.lower() for prefix in ["Category:", "Help:", "Wikipedia:", "Template:", "Template talk:", "Portal:", "List"] 
                for keyword in ["election", "conference"]
            )]
            return links
        return []

    def bfs(start, end, max_depth):
        queue = deque([(start, [start])])
        cached_links = {}
        visited = set()  # Track visited articles

        while queue:
            current, path = queue.popleft()
            print(current)
            if current == end:
                return path
            if len(path) <= max_depth:
                if current not in visited:
                    visited.add(current)
                    if current not in cached_links:
                        cached_links[current] = get_links(current)

                    # Batch fetching links to reduce overhead
                    links_to_fetch = [link for link in cached_links[current] if link not in path]

                    # Using ThreadPoolExecutor to parallelize link fetching
                    with ThreadPoolExecutor(max_workers=16) as executor:
                        futures = [executor.submit(lambda x: (x, path + [x]), link) for link in links_to_fetch]

                        for future in futures:
                            result = future.result()
                            if result[0] == end:
                                return result[1]

                            queue.append(result)

        return None


    start_time = time.time()
    path = bfs(start_title, end_title, max_depth)
    end_time = time.time()

    if path:
        print(f"Found a path from '{start_title}' to '{end_title}':")
        for i, step in enumerate(path):
            print(f"Step {i+1}: {step}")
    else:
        print(f"No path found from '{start_title}' to '{end_title}' within depth {max_depth}.")
    
    print(f"Execution time: {end_time - start_time:.2f} seconds")

# Example usage
start_article = "Susan B. Anthony"
end_article = "Avian influenza"
find_shortest_path(start_article, end_article)
