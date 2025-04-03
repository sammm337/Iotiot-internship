# Knowledge Graph Script

## Overview
This script builds a **Knowledge Graph (KG)** for the **H&M** clothing brand using **NetworkX**. It structures information about **product categories, individual products, features, marketing campaigns, and brand values**. The graph is then exported to a JSON file and used to process customer queries.

---
## What the Script Does:

## 1. Builds the Knowledge Graph
- Takes input data from `brand.json`   
- Adds a **brand node** for **H&M**.  
- Defines **product categories** (e.g., **Jackets, Footwear, Accessories**).  
- Adds **products** under each category (e.g., **"H&M Hoodie"** under **"Jackets"**).  
- Establishes **features** for products (e.g., **"Waterproof"** for jackets).  
- Links **marketing campaigns** (e.g., **"Winter Sale"**) to relevant products.  

## 2. Exports the Graph to JSON  
- Stores the **KG structure** in `knowledge_graph.json`.  

## 3. Processes Queries from `queries.json`  
- Sends a structured prompt that contains the knowledge graph and queries to gemini api to searche the graph for **relevant information**.  
 
## 4. Writes Results to `output.json`  
- Stores **responses** to each query in a structured **JSON format**.
---
## Components:

## `input.json`
This file contains a list of queries that users may ask about **H&M products, prices, features, campaigns, and categories**.
Example:
```json
 [
    "What is the price of H&M Denim Jacket?",
    "What are the features of H&M Sneakers?",
  ]

```

## `brand.json`
This file contains all the data points related to the brand.
```json
"brand": {
    "name": "H&M",
    "values": ["Affordability", "Sustainability", "Fashion-forward"]
  },
  "products": {
    "clothing": [
      {
        "id": "HM-CS-001",
        "name": "H&M Casual Shirt",
        "price": 29.99,
      }
    ],
      "footwear": [
      {
        "id": "HM-SN-004",
        "name": "H&M Sneakers",
        "price": 59.99,
      }
    ]
      }
```
## `output.json`  

This file contains the results of processing the queries.  

## Example:  

```json
{
  "What is the price of H&M Denim Jacket?": "The price of H&M Denim Jacket is $49.99.",
  "What are the features of H&M Sneakers?": "H&M Sneakers contain Breathable, Lightweight.",
  "What is the best product from H&M?": "The most premium product is H&M Leather Jacket priced at $129.99."

}
```
---
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
5. Run the script:
```bash
python main.py
```
6. View the generated output files:
```text
knowledge_graph.json - Structured knowledge graph
output.json - Processed query results
```
---
## In case of bugs contact me at : `samruddhis307@gmail.com`
---
## Credits and acknowledgements

This project was developed as part of my internship, where I worked on creating a knowledge graph for brand knowledge and context capture. I sincerely appreciate IoTIoT for providing the opportunity and guidance throughout this project. A special thanks to Nikhil Bhaskaran, Founder of IoTIoT, whose mentorship and technical insights greatly enhanced my understanding of knowledge graphs and query resolution. I also extend my gratitude to Sneha Bhapkar for her continuous support and encouragement during the development process. This project not only strengthened my skills in Python but also deepened my knowledge of data visualisation and customer support automation.

---
## Link to the project repo : `https://gitlab.iotiot.in/interns-projects/ragforbrands-samruddhi`
