# GeoPackager
## A Python module for performing CRUD operations on OGC GeoPackages

## Author: Alec Marshall, 2023

## Basic Functionality
GeoPackager is a basic, minimal interface for interacting with OGC GeoPackages. It facilitates quickly reading, creating, and modifying GeoPackages. 

To create or read a GeoPackage, import the `GeoPackage` class from `GeoPackager`. Then, create a new instance of the class, passing in a file path for the GeoPackage you'd like to connect to. If there is no GeoPackage at the specified path, it will create one.

