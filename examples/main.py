from expergen import create_dataclass, generate_variations, save_to_json_files

# Example usage
if __name__ == "__main__":
    field_definitions = {
        "param1": int,
        "param2": str,
        "param3": float
    }
    DynamicDataClass = create_dataclass("DynamicData", field_definitions)

    original_instance = DynamicDataClass(param1=10, param2="A", param3=3.14)

    variation_params = {
        "param1": [10, 20, 30],
        "param2": ["A", "B"],
        "param3": [3.14, 2.71]
    }

    variations = generate_variations(original_instance, variation_params)

    # Save variations to individual JSON files
    save_to_json_files(variations, "output_directory")
