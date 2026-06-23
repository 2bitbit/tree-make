# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "plotly",
#     "kaleido"
# ]
# ///

from make_tree import make_tree
from make_sunburst import make_sunburst


def main():
    make_tree()
    make_sunburst()


if __name__ == "__main__":
    main()
