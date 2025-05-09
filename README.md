# KevinBacon
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/ArchooD2/KevinBacon)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/ArchooD2/KevinBacon)
![GitHub top language](https://img.shields.io/github/languages/top/ArchooD2/KevinBacon)
![GitHub Issues or Pull Requests by label](https://img.shields.io/github/issues/ArchooD2/KevinBacon/good%20first%20issue)



Python Script to detect the fastest way between a start and end Wikipedia article.

## Description

KevinBacon is a Python script designed to find the shortest path between two Wikipedia articles. It uses the Wikipedia API to travel through links and determine the quickest route from the starting article to the destination article.

Uses [snaparg](https://github.com/ArchooD2/snaparg)!

## Features

- Pathfinding between Wikipedia articles
- Skips unnecessary categories and pages (e.g., "Help:", "Wikipedia:")

## Usage

1. Clone the repository:
    ```sh
    git clone https://github.com/ArchooD2/KevinBacon.git
    ```
2. Navigate to the project directory:
    ```sh
    cd KevinBacon
    ```
3.
    a. Run the requirements file:
    ```sh
    pip install -r requirements.txt
    ```
    b. Run the script:
    ```sh
    python baconwaffle.py "start article" "end article" "depth"
    ```
   c. Run the GUIscript:
    ```sh
    python bacongui.py
    ```

## Scripts

### baconwaffle.py

This script uses a breadth-first search (BFS) algorithm to find the shortest path between Wikipedia articles.

## Optimization

I want this to be optimized, so any suggestions or contributions to enhance the performance and efficiency of the script (or new scripts) are welcome!
See the [CONTRIBUTING.md](CONTRIBUTING.md) file for detailed guidelines on how to contribute.

## Contributing

This project is open for public use. Feel free to fork the repository, make improvements, and submit pull requests. If you use this in a project, just credit me somewhere!

## License

This project is licensed under the GPLv3.0 License. See the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or suggestions, please open an Issue!

---

Thank you for checking out KevinBacon! Happy pathfinding!
