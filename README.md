# ssg (Static Site Generator)

Command Line tool to turn markdown into html files. Check out the live demo here ![]()

## Description

This a command line tool built in plain Python3 that allows anyone to turn markdown into a functional static site. Some of the challenges while building this project was how to go about parsing html and structing the tree for HTML generation, along with making extensive unit tests. I hope to add to this project in the future support for nested markdown and tables.

## Installation

To install the project run this in your terminal

```bash
git clone https://github.com/bthomas218/ssg
cd ssg
```

## Usage

### Main

This is a shell script that builds the website to your localhost for testing. To run the command use:

```bash
./main.sh
```

### Build

This is a shell script that builds the website for deploying on github pages

```bash
./build.sh
```
