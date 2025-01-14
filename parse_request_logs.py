import re
from statistics import mean, median


def parse_log_file(log_file_path):
    start_times = {}
    end_times = {}
    durations = []

    # Regular expressions for start and end log entries
    start_pattern = re.compile(r"INFO:root:(.+?) start: (\d+\.\d+)")
    end_pattern = re.compile(r"INFO:root:(.+?) end: (\d+\.\d+)")

    # Read and parse the log file
    with open(log_file_path, 'r') as file:
        for line in file:
            start_match = start_pattern.search(line)
            end_match = end_pattern.search(line)

            if start_match:
                request_id, start_time = start_match.groups()
                start_times[request_id] = float(start_time)

            if end_match:
                request_id, end_time = end_match.groups()
                end_times[request_id] = float(end_time)

    # Calculate durations
    for request_id in start_times:
        if request_id in end_times:
            duration = end_times[request_id] - start_times[request_id]
            durations.append(duration)
            print(f"Request ID: {request_id}")
            print(f"  Start Time: {start_times[request_id]}")
            print(f"  End Time: {end_times[request_id]}")
            print(f"  Duration: {duration:.2f} seconds\n")
        else:
            print(f"Missing end time for Request ID: {request_id}")

    # Calculate and print statistics
    if durations:
        avg_duration = mean(durations)
        median_duration = median(durations)
        total_duration = sum(durations)

        print(f"Total Requests: {len(durations)}")
        print(f"Average Duration: {avg_duration:.2f} seconds")
        print(f"Median Duration: {median_duration:.2f} seconds")
        print(f"Total Duration: {total_duration:.2f} seconds")
    else:
        print("No complete request pairs found.")


# Example usage
parse_log_file('request_times.log')
