import docker

# Create a Docker client
client = docker.from_env()

# Build the Docker image
print("Building image from Dockerfile...")
client.images.build(path=".", tag="flask-apparmor")

# Run the container with the AppArmor profile
print("\nRunning container with AppArmor profile...")
container = client.containers.run(
    "flask-apparmor",
    ports={"5000/tcp": 5000},
    security_opt=["apparmor=my-apparmor-profile"],
    detach=True
)

try:
    print(f"Container started: {container.short_id}")

    # Verify that the AppArmor profile is configured
    print("\nInspecting container to verify AppArmor profile...")
    container_info = client.api.inspect_container(container.id)
    apparmor_profile = container_info["HostConfig"]["SecurityOpt"]

    print(f"AppArmor profile applied: {apparmor_profile}")

finally:
    # Stop the container
    print("\nStopping the container...")
    container.stop()
    print("Container stopped.")
