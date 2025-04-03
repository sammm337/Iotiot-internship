import json
import os
import google.generativeai as genai
from datetime import datetime
import networkx as nx
import time
from typing import Dict, List, Union, Any

# Configuration
API_KEY = os.environ.get("GEMINI_API_KEY", "your-api-key")
genai.configure(api_key=API_KEY)

def load_json_file(file_path: str) -> Union[Dict, List, None]:
    """Load data from a JSON file with enhanced error handling."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if not isinstance(data, (dict, list)):
                raise ValueError("JSON file should contain an object or array")
            return data
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {file_path}: {e}")
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
    return None

def save_json_file(data: Any, file_path: str) -> bool:
    """Save data to a JSON file with improved error handling."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        print(f"Data successfully saved to {file_path}")
        return True
    except Exception as e:
        print(f"Error saving to {file_path}: {e}")
        return False

class EnhancedKnowledgeGraph:
    """A more sophisticated knowledge graph implementation with advanced capabilities."""
    
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.node_counter = 0
        self.edge_counter = 0
    
    def add_node(self, node_id: str, node_type: str, **attrs) -> None:
        """Add a node with type and attributes."""
        if not isinstance(node_id, str):
            node_id = str(node_id)
        attrs['type'] = node_type
        self.graph.add_node(node_id, **attrs)
    
    def add_edge(self, source: str, target: str, relation: str, **attrs) -> None:
        """Add a directed edge with relation type and attributes."""
        if source and target:  # Ensure both source and target are valid
            self.graph.add_edge(source, target, key=self.edge_counter, relation=relation, **attrs)
            self.edge_counter += 1
    
    def add_complex_structure(self, parent_id: str, data: Any, relation_prefix: str = "") -> None:
        """
        Recursively add complex nested structures to the graph.
        Handles dictionaries, lists, and primitive values.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                node_id = f"{parent_id}_{key}" if parent_id else key
                self.add_node(node_id, "attribute")
                self.add_edge(parent_id, node_id, f"{relation_prefix}{key}")
                self.add_complex_structure(node_id, value, relation_prefix)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                node_id = f"{parent_id}_{i}"
                self.add_node(node_id, "list_item")
                self.add_edge(parent_id, node_id, f"{relation_prefix}item_{i}")
                self.add_complex_structure(node_id, item, relation_prefix)
        else:
            # Primitive value - store the actual value directly
            self.add_node(parent_id, self.graph.nodes[parent_id]['type'], value=data)

    def to_serializable(self) -> Dict[str, List[Dict]]:
        """Convert the graph to a JSON-serializable format with enhanced metadata."""
        serialized = {
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "node_count": self.graph.number_of_nodes(),
                "edge_count": self.graph.number_of_edges(),
                "graph_type": "EnhancedKnowledgeGraph"
            },
            "nodes": [],
            "edges": []
        }
        
        for node, attrs in self.graph.nodes(data=True):
            node_data = {"id": node}
            node_data.update(attrs)
            serialized["nodes"].append(node_data)
        
        for source, target, key, attrs in self.graph.edges(data=True, keys=True):
            edge_data = {
                "source": source,
                "target": target,
                "key": key
            }
            edge_data.update(attrs)
            serialized["edges"].append(edge_data)
        
        return serialized

def create_enhanced_knowledge_graph(brand_data: Dict) -> Dict:
    """
    Create a sophisticated knowledge graph from brand data with improved structure
    """
    kg = EnhancedKnowledgeGraph()
    
    # Extract brand info
    brand_info = brand_data.get("brand", {})
    if not isinstance(brand_info, dict):
        raise TypeError("Expected 'brand' field to be a dictionary")
    
    # Add brand as root node
    brand_name = brand_info.get("name", "Unknown_Brand")
    kg.add_node(brand_name, "brand")
    
    # Process all brand attributes
    for key, value in brand_info.items():
        if key == "name":
            continue
        
        attr_node = f"{brand_name}_{key}"
        kg.add_node(attr_node, "attribute")
        kg.add_edge(brand_name, attr_node, f"has_{key}")
        
        if isinstance(value, (dict, list)):
            kg.add_complex_structure(attr_node, value)
        else:
            kg.add_node(attr_node, "attribute", value=value)

    # PRODUCTS - Direct connection to product nodes for better querying
    if "products" in brand_data and isinstance(brand_data["products"], dict):
        # Create products node
        products_node = f"{brand_name}_products"
        kg.add_node(products_node, "product_category")
        kg.add_edge(brand_name, products_node, "has_products")
        
        # Process each product category
        for category, products_list in brand_data["products"].items():
            category_node = f"{products_node}_{category}"
            kg.add_node(category_node, "category", name=category)
            kg.add_edge(products_node, category_node, "has_category")
            
            if isinstance(products_list, list):
                for product in products_list:
                    if isinstance(product, dict) and "name" in product:
                        product_id = product.get("id", f"unknown_id_{product['name']}")
                        product_name = product["name"]
                        
                        # Add product node with direct values
                        kg.add_node(product_name, "product", 
                                   id=product_id,
                                   price=product.get("price"),
                                   category=product.get("category"))
                        
                        # Connect product to category
                        kg.add_edge(category_node, product_name, "contains_product")
                        kg.add_edge(product_name, category_node, "belongs_to_category")
                        
                        # Direct connection from brand to product
                        kg.add_edge(brand_name, product_name, "sells")
                        
                        # Process attributes
                        for key, value in product.items():
                            if key in ["name", "id", "price", "category"]:
                                continue  # These are already stored directly
                            
                            attr_node = f"{product_name}_{key}"
                            
                            if isinstance(value, list):
                                # Special handling for features, materials, etc.
                                kg.add_node(attr_node, "product_attribute", name=key)
                                kg.add_edge(product_name, attr_node, f"has_{key}")
                                
                                for i, item in enumerate(value):
                                    item_node = f"{attr_node}_{i}"
                                    kg.add_node(item_node, "attribute_value", value=item)
                                    kg.add_edge(attr_node, item_node, "contains")
                            else:
                                # Direct attribute
                                kg.add_node(attr_node, "product_attribute", name=key, value=value)
                                kg.add_edge(product_name, attr_node, f"has_{key}")
    
    # CAMPAIGNS - With direct product connections
    if "campaigns" in brand_data and isinstance(brand_data["campaigns"], list):
        # Create campaigns container
        campaigns_node = f"{brand_name}_campaigns"
        kg.add_node(campaigns_node, "campaigns_container")
        kg.add_edge(brand_name, campaigns_node, "has_campaigns")
        
        for campaign in brand_data["campaigns"]:
            if isinstance(campaign, dict) and "name" in campaign:
                campaign_name = campaign["name"]
                # Add campaign with direct attributes
                kg.add_node(campaign_name, "campaign", 
                           period=campaign.get("period"),
                           discount=campaign.get("discount"))
                
                kg.add_edge(campaigns_node, campaign_name, "contains")
                kg.add_edge(brand_name, campaign_name, "runs")
                
                # Process included products
                if "included_products" in campaign and isinstance(campaign["included_products"], list):
                    included_node = f"{campaign_name}_included_products"
                    kg.add_node(included_node, "product_list")
                    kg.add_edge(campaign_name, included_node, "includes")
                    
                    for product_name in campaign["included_products"]:
                        # Direct connections to products
                        kg.add_edge(campaign_name, product_name, "features")
                        kg.add_edge(product_name, campaign_name, "featured_in")
                        
                        # Also add to the collection
                        kg.add_edge(included_node, product_name, "contains")
                
                # Process new arrivals
                if "new_arrivals" in campaign and isinstance(campaign["new_arrivals"], list):
                    arrivals_node = f"{campaign_name}_new_arrivals"
                    kg.add_node(arrivals_node, "product_list")
                    kg.add_edge(campaign_name, arrivals_node, "introduces")
                    
                    for product_name in campaign["new_arrivals"]:
                        # Direct connections
                        kg.add_edge(campaign_name, product_name, "introduces")
                        kg.add_edge(product_name, campaign_name, "introduced_in")
                        
                        # Add to collection
                        kg.add_edge(arrivals_node, product_name, "contains")
                
                # Add campaign themes
                if "themes" in campaign and isinstance(campaign["themes"], list):
                    themes_node = f"{campaign_name}_themes"
                    kg.add_node(themes_node, "theme_list")
                    kg.add_edge(campaign_name, themes_node, "has_themes")
                    
                    for i, theme in enumerate(campaign["themes"]):
                        theme_node = f"{themes_node}_{i}"
                        kg.add_node(theme_node, "theme", value=theme)
                        kg.add_edge(themes_node, theme_node, "contains")
    
    # STORE INFO
    if "store_info" in brand_data and isinstance(brand_data["store_info"], dict):
        store_node = f"{brand_name}_store_info"
        kg.add_node(store_node, "store_info")
        kg.add_edge(brand_name, store_node, "has_store_info")
        
        # Store layout - direct connections
        if "layout" in brand_data["store_info"]:
            layout_node = f"{store_node}_layout"
            kg.add_node(layout_node, "store_layout")
            kg.add_edge(store_node, layout_node, "has_layout")
            
            for section, location in brand_data["store_info"]["layout"].items():
                section_node = f"{layout_node}_{section}"
                kg.add_node(section_node, "section", name=section, location=location)
                kg.add_edge(layout_node, section_node, "contains")
                kg.add_edge(section_node, layout_node, "part_of")
        
        # Store services
        if "services" in brand_data["store_info"]:
            services_node = f"{store_node}_services"
            kg.add_node(services_node, "service_list")
            kg.add_edge(store_node, services_node, "offers")
            
            for i, service in enumerate(brand_data["store_info"]["services"]):
                service_node = f"{services_node}_{i}"
                kg.add_node(service_node, "service", value=service)
                kg.add_edge(services_node, service_node, "contains")
    
    # PROMOTIONS
    if "current_promotions" in brand_data and isinstance(brand_data["current_promotions"], list):
        promos_node = f"{brand_name}_promotions"
        kg.add_node(promos_node, "promotions")
        kg.add_edge(brand_name, promos_node, "has_promotions")
        
        for i, promo in enumerate(brand_data["current_promotions"]):
            promo_node = f"{promos_node}_{i}"
            
            # Store promotion with direct values
            kg.add_node(promo_node, "promotion",
                      discount=promo.get("discount"),
                      valid_until=promo.get("valid_until"),
                      promo_code=promo.get("promo_code"))
            
            kg.add_edge(promos_node, promo_node, "contains")
            
            # Handle product-specific promotions
            if "product_ids" in promo:
                for product_id in promo["product_ids"]:
                    # Find product name by ID
                    for node in kg.graph.nodes():
                        if kg.graph.nodes[node].get("type") == "product" and \
                           kg.graph.nodes[node].get("id") == product_id:
                            kg.add_edge(promo_node, node, "applies_to")
                            kg.add_edge(node, promo_node, "has_promotion")
            
            # Handle category promotions
            if "category" in promo:
                category_value = promo["category"]
                kg.add_node(f"{promo_node}_category", "promo_category", value=category_value)
                kg.add_edge(promo_node, f"{promo_node}_category", "applies_to_category")
    
    # PRODUCT FEATURES - Direct connections
    if "product_features" in brand_data and isinstance(brand_data["product_features"], dict):
        for feature, products in brand_data["product_features"].items():
            feature_node = f"{brand_name}_feature_{feature}"
            kg.add_node(feature_node, "product_feature", name=feature)
            kg.add_edge(brand_name, feature_node, "offers_feature")
            
            for product_name in products:
                kg.add_edge(feature_node, product_name, "applies_to")
                kg.add_edge(product_name, feature_node, "has_feature")
    
    # CATALOG
    if "full_product_catalog" in brand_data and isinstance(brand_data["full_product_catalog"], dict):
        catalog_node = f"{brand_name}_catalog"
        kg.add_node(catalog_node, "product_catalog")
        kg.add_edge(brand_name, catalog_node, "has_catalog")
        
        for category, items in brand_data["full_product_catalog"].items():
            category_node = f"{catalog_node}_{category}"
            kg.add_node(category_node, "product_category", name=category)
            kg.add_edge(catalog_node, category_node, "includes")
            
            for i, item in enumerate(items):
                item_node = f"{category_node}_{i}"
                kg.add_node(item_node, "catalog_item", value=item)
                kg.add_edge(category_node, item_node, "lists")
    
    # Add special semantic connections
    _add_inferred_relationships(kg, brand_name, brand_data)
    
    return kg.to_serializable()

def _add_inferred_relationships(kg: EnhancedKnowledgeGraph, brand_name: str, brand_data: Dict) -> None:
    """Add additional semantic relationships that link data in meaningful ways"""
    
    # Connect products to categorical features
    if "product_features" in brand_data:
        for feature, product_names in brand_data["product_features"].items():
            for product_name in product_names:
                # Create feature-specific tags
                tag_node = f"tag_{feature}"
                if not kg.graph.has_node(tag_node):
                    kg.add_node(tag_node, "tag", name=feature)
                    
                kg.add_edge(product_name, tag_node, "tagged_as")
                
                # Example: Link water-resistant products to rainy weather use case
                if feature.lower() == "water_resistant":
                    use_case = "rainy_weather"
                    use_case_node = f"use_case_{use_case}"
                    if not kg.graph.has_node(use_case_node):
                        kg.add_node(use_case_node, "use_case", name="rainy weather")
                    kg.add_edge(product_name, use_case_node, "suitable_for")
                
                # Connect formal wear
                if feature.lower() == "formal_wear":
                    formal_cat = "formal_wear"
                    formal_node = f"category_{formal_cat}"
                    if not kg.graph.has_node(formal_node):
                        kg.add_node(formal_node, "category", name="Formal Wear")
                    kg.add_edge(product_name, formal_node, "belongs_to")
    
    # Link products to their location in store
    if "store_info" in brand_data and "layout" in brand_data["store_info"]:
        store_layout = brand_data["store_info"]["layout"]
        
        # Connect all products to their section locations
        for product_node in [n for n in kg.graph.nodes() if kg.graph.nodes[n].get("type") == "product"]:
            # Get product category
            product_category = kg.graph.nodes[product_node].get("category")
            
            if product_category:
                # Find matching section
                for section, location in store_layout.items():
                    if section.lower() in product_category.lower():
                        location_node = f"{brand_name}_store_location_{section}"
                        if not kg.graph.has_node(location_node):
                            kg.add_node(location_node, "store_location", name=section, location=location)
                        kg.add_edge(product_node, location_node, "located_at")
    
    # Connect campaign products to themes
    if "campaigns" in brand_data:
        for campaign in brand_data["campaigns"]:
            if "name" in campaign and "themes" in campaign:
                campaign_name = campaign["name"]
                
                # Get products in campaign
                product_lists = []
                if "included_products" in campaign:
                    product_lists.append(campaign["included_products"])
                if "new_arrivals" in campaign:
                    product_lists.append(campaign["new_arrivals"])
                
                # Connect each product to themes
                for product_list in product_lists:
                    for product_name in product_list:
                        for i, theme in enumerate(campaign["themes"]):
                            theme_node = f"{campaign_name}_theme_{i}"
                            if not kg.graph.has_node(theme_node):
                                kg.add_node(theme_node, "theme", value=theme)
                            kg.add_edge(product_name, theme_node, "has_theme")

def process_query_with_gemini(query: str, knowledge_graph: Dict) -> str:
    """
    Enhanced query processing with improved prompt structure
    """
    # Create a curated subset of the graph for the prompt
    nodes_sample = json.dumps([n for n in knowledge_graph['nodes'][:30]], indent=2)
    edges_sample = json.dumps([e for e in knowledge_graph['edges'][:30]], indent=2)
    
    # Get important product information
    products = [node for node in knowledge_graph['nodes'] 
                if node.get('type') == 'product']
    product_summary = json.dumps(products, indent=2)
    
    # Get promotions
    promotions = [node for node in knowledge_graph['nodes'] 
                 if node.get('type') == 'promotion']
    promo_summary = json.dumps(promotions, indent=2)
    
    # Get campaigns
    campaigns = [node for node in knowledge_graph['nodes'] 
                if node.get('type') == 'campaign']
    campaign_summary = json.dumps(campaigns, indent=2)
    
    # More focused prompt with essential information
    prompt = f"""
    Brand Knowledge Graph Query System

    You are a knowledge graph query system for H&M brand data. Your task is to answer queries by analyzing the knowledge graph data provided.
    
    GRAPH METADATA:
    {json.dumps(knowledge_graph['metadata'], indent=2)}
    
    NODE TYPE SUMMARY:
    {_get_node_type_summary(knowledge_graph)}
    
    QUERY: {query}
    
    RELEVANT INFORMATION FROM KNOWLEDGE GRAPH:
    
    Products:
    {product_summary}
    
    Campaigns:
    {campaign_summary}
    
    Promotions:
    {promo_summary}
    
    Sample Nodes:
    {nodes_sample}
    
    Sample Edges:
    {edges_sample}
    
    INSTRUCTIONS:
    1. Answer the query using ONLY information from the graph data provided
    2. Include specific details like prices, features, and attributes when relevant
    3. If the information isn't explicitly in the graph, say "I couldn't find that information"
    4. Format your answer in a clear, direct way
    
    Your response format:
    - Answer: [your detailed answer]
    - Sources: [list specific node IDs or data points used]
    - Confidence: [high/medium/low]
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error processing query: {str(e)}"

def _get_node_type_summary(knowledge_graph: Dict) -> str:
    """Generate a summary of node types in the graph."""
    type_counts = {}
    for node in knowledge_graph.get("nodes", []):
        node_type = node.get("type", "unknown")
        type_counts[node_type] = type_counts.get(node_type, 0) + 1
    
    summary = ["Node Type Summary:"]
    for type_name, count in sorted(type_counts.items()):
        summary.append(f"- {type_name}: {count} nodes")
    
    return "\n".join(summary)

def main():
    """Enhanced main function with better progress tracking and error handling."""
    print("Starting knowledge graph processing...")
    start_time = time.time()
    
    try:
        # Load brand data with validation
        print("Loading brand data...")
        brand_data = load_json_file("brand.json")
        if not brand_data:
            raise ValueError("Failed to load brand data")
        
        # Create enhanced knowledge graph
        print("Creating knowledge graph...")
        knowledge_graph = create_enhanced_knowledge_graph(brand_data)
        
        # Save knowledge graph with backup
        print("Saving knowledge graph...")
        if not save_json_file(knowledge_graph, "knowledge_graph.json"):
            raise RuntimeError("Failed to save knowledge graph")
        
        # Create a test query file if it doesn't exist
        if not os.path.exists("queries.json"):
            print("Creating sample queries file...")
            sample_queries = [
                "What's the price of the H&M Casual Shirt?",
                "What makes the H&M Denim Jacket special?",
                "How do I use the H&M Moisturizing Cream?",
                "Where can I find H&M Sneakers in the store?",
                "Are H&M Cargo Pants on sale right now?",
                "What's included in the WinterFashion2024 campaign?",
                "Do you have any formal wear at H&M?", 
                "Which H&M products are good for rainy weather?",
                "What's H&M famous for?",
                "Can you show me everything H&M sells?",
                "Which items in the WinterFashion2024 collection are good for rain?",
                "What kind of shoes does H&M have?",
                "Are there any discounts on leather items at H&M?",
                "What's new in the summer collection at H&M?"
            ]
            save_json_file(sample_queries, "queries.json")
        
        # Load queries
        print("Loading queries...")
        queries = load_json_file("queries.json")
        if not queries or not isinstance(queries, list):
            raise ValueError("Invalid queries format - expected a list")
        
        # Process queries with progress tracking
        print(f"Processing {len(queries)} queries...")
        results = {
            "metadata": {
                "start_time": datetime.now().isoformat(),
                "query_count": len(queries)
            },
            "responses": []
        }
        
        for i, query in enumerate(queries, 1):
            try:
                print(f"\nProcessing query {i}/{len(queries)}: {query[:50]}...")
                start_query = time.time()
                
                response = process_query_with_gemini(query, knowledge_graph)
                
                results["responses"].append({
                    "query": query,
                    "response": response,
                    "processing_time": time.time() - start_query
                })
                
                # Respect rate limits
                if i < len(queries):
                    time.sleep(1.5)  # More conservative delay
                
            except Exception as e:
                print(f"Error processing query {i}: {e}")
                results["responses"].append({
                    "query": query,
                    "error": str(e)
                })
        
        # Save final results
        print("Saving results...")
        results["metadata"]["end_time"] = datetime.now().isoformat()
        results["metadata"]["total_time"] = time.time() - start_time
        
        if not save_json_file(results, "output.json"):
            raise RuntimeError("Failed to save results")
        
        print(f"\nCompleted successfully in {time.time() - start_time:.2f} seconds")
    
    except Exception as e:
        print(f"\nFatal error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())