
# BestFork

## Overview

BestFork is a Python-based CLI tool designed to identify and prioritize the best developers who have forked a specific GitHub repository. By analyzing the "Amount of Change" and the last update time, BestFork sorts potential contributors who could be valuable additions to the original project's community.

## Features

- Retrieves a list of forks for a given GitHub repository.
- Calculates an "Amount of Change" score for each fork based on commits, lines added, and lines removed.
- Generates a CSV file listing fork owners, their emails, and other relevant details, sorted by their potential value as contributors.

## Installation

```bash
pip install requests click subprocess32
```

## Usage

Run the following command:

```bash
python get_forks.py
```

## Why BestFork?

### Recruitment of Quality Developers

One of the main challenges in open-source development is identifying developers who can contribute meaningfully to a project. BestFork helps maintainers:

1. **Identify Top Contributors**: Sort developers based on their activity and the magnitude of their contributions to their forks.
2. **Engage Potential Contributors**: Use the provided contact information to reach out to potential contributors.
3. **Code Review**: Offer to review significant changes from potential contributors, opening the door for future collaboration.

## Contributing

We welcome contributions to BestFork. If you're a developer interested in contributing to the original project that this tool analyzes, please reach out—we're actively looking for talented developers to enrich our community.
