from pathlib import Path

from link_extractor.scanner import scan_folder


def get_scan_results(folder_path: Path) -> dict[str, set[str]]:
    if not folder_path.exists() or not folder_path.is_dir():
        raise ValueError("Invalid folder path.")

    return scan_folder(folder_path)


def main() -> None:
    folder_input = input("Enter folder path: ").strip()
    folder_path = Path(folder_input)

    try:
      results = get_scan_results(folder_path)
    except ValueError as exc:
      print(str(exc))
      return

    if not results:
        print("No GitHub links found.")
        return

    all_links: set[str] = set()

    print("\nGitHub links by file:\n")
    for file_name, links in sorted(results.items()):
        print(file_name)
        for link in sorted(links):
            print(f"  {link}")
            all_links.add(link)
        print()


if __name__ == "__main__":
    main()