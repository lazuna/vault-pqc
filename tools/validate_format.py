import os, yaml, sys

REQUIRED = ["README.md", "meta.yaml", "_index.yaml", "LICENSE"]
LICENSES = ["MIT", "CC-BY-4.0", "CC-BY-NC-SA-4.0"]

def validate():
    missing = [f for f in REQUIRED if not os.path.exists(f)]
    if missing:
        print("Missing required files:", ", ".join(missing))
        sys.exit(1)

    with open("meta.yaml") as f:
        meta = yaml.safe_load(f)
        if meta["license"] not in LICENSES:
            print("Invalid license:", meta["license"])
            sys.exit(1)

    print("✅ Format is valid.")

if __name__ == "__main__":
    validate()
