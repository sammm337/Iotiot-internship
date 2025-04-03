# H&M Knowledge Graph Script

## Overview
This script builds a **Knowledge Graph (KG)** for the **H&M** clothing brand using **NetworkX**. It structures information about **product categories, individual products, features, marketing campaigns, and brand values**. The graph is then exported to a JSON file and used to process customer queries.

---

## `input.json`
This file contains a list of queries that users may ask about **H&M products, prices, features, campaigns, and categories**.

Example:
```json
{
  "queries": [
    "What is the price of H&M Denim Jacket?",
    "What are the features of H&M Sneakers?",
    "What is the best product from H&M?",
    "Tell me about the Summer Collection campaign.",
    "List all available products from H&M."
  ]
}
```

## What the Script Does:

## 1. Builds the Knowledge Graph  
- Adds a **brand node** for **H&M**.  
- Defines **product categories** (e.g., **Jackets, Footwear, Accessories**).  
- Adds **products** under each category (e.g., **"H&M Hoodie"** under **"Jackets"**).  
- Establishes **features** for products (e.g., **"Waterproof"** for jackets).  
- Links **marketing campaigns** (e.g., **"Winter Sale"**) to relevant products.  

## 2. Exports the Graph to JSON  
- Stores the **KG structure** in `knowledge_graph.json`.  

## 3. Processes Queries from `input.json`  
- Reads queries and searches the graph for **relevant information**.  
- Extracts details such as **price, features, discounts, and categories**.  

## 4. Writes Results to `output.json`  
- Stores **responses** to each query in a structured **JSON format**.  

## `output.json`  

This file contains the results of processing the queries.  

## Example:  

```json
{
  "What is the price of H&M Denim Jacket?": "The price of H&M Denim Jacket is $49.99.",
  "What are the features of H&M Sneakers?": "H&M Sneakers contain Breathable, Lightweight.",
  "What is the best product from H&M?": "The most premium product is H&M Leather Jacket priced at $129.99.",
  "Tell me about the Summer Collection campaign.": "The Summer Collection campaign offers 20% discount on H&M T-Shirt, H&M Sneakers. It runs from June 1 to July 31.",
  "List all available products from H&M.": "H&M offers the following products: H&M Hoodie, H&M Denim Jacket, H&M Leather Jacket, H&M Sneakers, H&M Running Shoes, H&M Handbag, H&M Sunglasses."
}
```

## How to use the script
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Set your Gemini API key:

```bash
export GEMINI_API_KEY="your-api-key-here"
```
3. File Structure
```text
project/
├── brand.json            # Input brand data
├── queries.json         # List of queries to process
├── knowledge_graph.json # Generated knowledge graph
├── output.json          # Query results
├── new.py               # Main script
└── README.md            # This file
```
4. Prepare your input files:
```text
brand.json - Your brand data in JSON format

queries.json - List of queries to process
```
5. View the generated output files:
```text
knowledge_graph.json - Structured knowledge graph

output.json - Processed query results
```