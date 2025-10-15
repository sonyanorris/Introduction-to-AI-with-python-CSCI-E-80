import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)
    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    total_pages = len(corpus)
    distribution = {}
    links = corpus[page]
    # If the current page has outgoing links, loop through each page in corpus
    if links:
        for p in corpus:
            # If a page is among links, assign probability
            if p in links:
                distribution[p] = ((1 - damping_factor) / len(corpus)) + (
                    damping_factor / len(links)
                )

            # If a page is not among links, assign probability
            else:
                distribution[p] = (1 - damping_factor) / len(corpus)

    # If the current page does not have outgoing links, assume equal probability to all pages
    else:
        for p in corpus:
            distribution[p] = 1 / total_pages

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize and populate a dictionary
    page_rank = {p: 0 for p in corpus}

    # Initialize a list of all pages from the corpus
    all_pages = list(corpus.keys())

    # Generate n samples
    for i in range(n):
        # If this is the 1st sample, choose uniformly at random
        if i == 0:
            current_page = random.choices(all_pages, k=1)[0]
        # If this is NOT the 1st sample, choose the next page based on probabilities from the transition model
        else:
            probabilities = transition_model(corpus, current_page, damping_factor)
            pages_list = list(probabilities.keys())
            weights_list = list(probabilities.values())
            current_page = random.choices(pages_list, weights_list, k=1)[0]

        # Increment count of selected pages by 1/n
        page_rank[current_page] += 1 / n

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize a dictionary for "previous" page ranks
    page_rank = dict()
    # Assign equal probability to each page to start with
    N = len(corpus)
    page_rank = {p: 1 / N for p in corpus}
    
    # Iteratively compute ranks until convergence
    while True:
        # Initialize a dictionary for updated page ranks
        new_rank = dict()
        # Compute the rank for each page
        for p in corpus:
            # Assign the "base" rank
            new_rank[p] = (1 - damping_factor) / N
            # Assign "additional" rank
            for linking_page in corpus:
                # If a page is a sink
                if len(corpus[linking_page]) == 0:
                    new_rank[p] += damping_factor * page_rank[linking_page] / N
                    
                # If a page has incoming links
                elif p in corpus[linking_page]:
                    num_links = len(corpus[linking_page])
                    new_rank[p] += damping_factor * page_rank[linking_page] / num_links

        # If all pages converged, return result
        if all(abs(new_rank[p] - page_rank[p]) < 0.001 for p in corpus):
            return new_rank

        # Otherwise, update page_rank and continue
        page_rank = new_rank.copy()


if __name__ == "__main__":
    main()
