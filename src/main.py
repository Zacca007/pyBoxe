def tkinter() -> None:
    """Launch Tkinter interface with new modular architecture."""
    from interface.window import Window
    window = Window()
    window.mainloop()


def console() -> None:
    """Run console version for testing the new architecture."""
    from core import FpiService, FpiWriter

    print("PyBoxe - Console Mode")
    print("=" * 50)

    # Initialize service
    service = FpiService()

    # Get user input
    try:
        min_matches = int(input("Enter minimum matches (default: 5): ") or "5")
        max_matches = int(input("Enter maximum matches (default: 20): ") or "20")
        filename = input("Enter filename (default: athletes): ").strip() or "athletes"

        # Optional: set filters
        print("\nAvailable committees:")
        for i, committee in enumerate(service.committees[:5], 1):  # Show first 5
            print(f"  {i}. {committee}")
        if len(service.committees) > 5:
            print(f"  ... and {len(service.committees) - 5} more")

        committee_choice = input("\nSelect committee (press Enter to skip): ").strip()
        if committee_choice.isdigit():
            idx = int(committee_choice) - 1
            if 0 <= idx < len(service.committees):
                service.update_committee(service.committees[idx])
                print(f"Selected committee: {service.committees[idx]}")

        print("\nAvailable qualifications:")
        for i, qual in enumerate(service.qualifications[:5], 1):  # Show first 5
            print(f"  {i}. {qual}")
        if len(service.qualifications) > 5:
            print(f"  ... and {len(service.qualifications) - 5} more")

        qual_choice = input("\nSelect qualification (press Enter to skip): ").strip()
        if qual_choice.isdigit():
            idx = int(qual_choice) - 1
            if 0 <= idx < len(service.qualifications):
                qual_name = list(service.qualifications)[idx]
                service.update_qualification(qual_name)
                print(f"Selected qualification: {qual_name}")

                # Show weights if available
                weights = service.weights
                if weights:
                    print("\nAvailable weights:")
                    for i, weight in enumerate(weights[:5], 1):  # Show first 5
                        print(f"  {i}. {weight}")
                    if len(weights) > 5:
                        print(f"  ... and {len(weights) - 5} more")

                    weight_choice = input("\nSelect weight (press Enter to skip): ").strip()
                    if weight_choice.isdigit():
                        w_idx = int(weight_choice) - 1
                        if 0 <= w_idx < len(weights):
                            service.update_weight(weights[w_idx])
                            print(f"Selected weight: {weights[w_idx]}")

        print(f"\nSearching athletes with {min_matches}-{max_matches} matches...")
        print("This may take a while...")

        # Create writer and search
        writer = FpiWriter(service, min_matches, max_matches, filename)
        writer.search_and_write()

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except ValueError as e:
        print(f"Invalid input: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == "console":
            console()
        else:
            tkinter()
    else:
        # Default to tkinter
        tkinter()