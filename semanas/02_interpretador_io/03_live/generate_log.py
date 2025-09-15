#!/usr/bin/env python3
import asyncio
import random
import datetime
import time
import os
from concurrent.futures import ThreadPoolExecutor

BATCH_SIZE = 10000
CONCURRENT_BATCHES = 10
WRITE_BUFFER_SIZE = 50 * 1024 * 1024  # 50MB
TARGET_SIZE_GB = 2
NUM_THREADS = 8

IPS = [
    f"{random.randint(1, 255)}.{random.randint(0, 255)}."
    f"{random.randint(0, 255)}.{random.randint(1, 255)}"
    for _ in range(1000)
]
METHODS = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]
PATHS = [
    "/",
    "/api/users",
    "/api/products",
    "/api/orders",
    "/api/auth",
    "/login",
    "/logout",
    "/dashboard",
    "/profile",
    "/settings",
    "/static/css/main.css",
    "/static/js/app.js",
    "/static/js/vendor.js",
    "/images/logo.png",
    "/images/banner.jpg",
    "/favicon.ico",
    "/api/v1/data",
    "/api/v2/users",
    "/health",
    "/metrics",
    "/admin/dashboard",
    "/admin/users",
    "/admin/settings",
    "/products/1234",
    "/products/5678",
    "/cart",
    "/checkout",
]
STATUS_CODES = [
    200,
    201,
    204,
    301,
    302,
    304,
    400,
    401,
    403,
    404,
    500,
    502,
    503,
]
USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
    "curl/7.68.0",
    "Python/3.9 aiohttp/3.7.4",
    "PostmanRuntime/7.28.4",
]
REFERERS = [
    "-",
    "https://example.com",
    "https://google.com",
    "https://github.com",
]


def generate_log_lines(count: int) -> str:
    lines = []
    for _ in range(count):
        ip = random.choice(IPS)
        timestamp = datetime.datetime.now() - datetime.timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )
        timestamp_str = timestamp.strftime("%d/%b/%Y:%H:%M:%S +0000")
        method = random.choice(METHODS)
        path = random.choice(PATHS)
        status = random.choice(STATUS_CODES)
        size = random.randint(100, 50000)
        referer = random.choice(REFERERS)
        user_agent = random.choice(USER_AGENTS)
        response_time = round(random.uniform(0.001, 5.0), 3)

        lines.append(
            f'{ip} - - [{timestamp_str}] "{method} {path} HTTP/1.1" {status} '
            f'{size} "{referer}" "{user_agent}" {response_time}\n'
        )

    return "".join(lines)


async def generate_batch(executor: ThreadPoolExecutor, batch_size: int) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, generate_log_lines, batch_size)


async def write_to_file(file_handle, data: str, stats: dict):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, file_handle.write, data)
    stats["bytes_written"] += len(data.encode("utf-8"))
    stats["lines_written"] += data.count("\n")


async def generate_nginx_log(
    filename: str = "nginx_sample.log", target_size_gb: float = 2
):
    target_size = int(target_size_gb * 1024 * 1024 * 1024)
    stats = {"bytes_written": 0, "lines_written": 0}

    print(f"Generating {target_size_gb}GB nginx log file...")
    print(
        f"Using {CONCURRENT_BATCHES} concur generators, {NUM_THREADS} threads"
    )

    start_time = time.time()
    last_report_time = start_time
    last_bytes = 0

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        with open(filename, "w", buffering=WRITE_BUFFER_SIZE) as f:
            pending_tasks = []

            while stats["bytes_written"] < target_size:
                # Keep queue filled with concurrent batch generations
                while (
                    len(pending_tasks) < CONCURRENT_BATCHES
                    and stats["bytes_written"] < target_size
                ):
                    task = asyncio.create_task(
                        generate_batch(executor, BATCH_SIZE)
                    )
                    pending_tasks.append(task)

                # Wait for at least one batch to complete
                done, pending = await asyncio.wait(
                    pending_tasks, return_when=asyncio.FIRST_COMPLETED
                )
                pending_tasks = list(pending)

                # Write completed batches
                for task in done:
                    batch_data = await task
                    await write_to_file(f, batch_data, stats)

                # Progress reporting
                current_time = time.time()
                if current_time - last_report_time >= 0.5:
                    elapsed = current_time - start_time
                    speed = (stats["bytes_written"] - last_bytes) / (
                        (current_time - last_report_time) * 1024 * 1024
                    )
                    avg_speed = stats["bytes_written"] / (
                        elapsed * 1024 * 1024
                    )
                    progress = (stats["bytes_written"] / target_size) * 100
                    gb_written = stats["bytes_written"] / (1024**3)

                    print(
                        f"\rProgress: {progress:.1f}% ({gb_written:.2f}GB) | "
                        f"Spd: {speed:.0f} MB/s | Avg: {avg_speed:.0f} MB/s | "
                        f"Lines: {stats['lines_written']:,}",
                        end="",
                        flush=True,
                    )

                    last_report_time = current_time
                    last_bytes = stats["bytes_written"]

            # Process any remaining tasks
            if pending_tasks:
                remaining = await asyncio.gather(*pending_tasks)
                for batch_data in remaining:
                    if stats["bytes_written"] < target_size:
                        await write_to_file(f, batch_data, stats)

    elapsed = time.time() - start_time
    final_size = os.path.getsize(filename)

    print(f"\n✓ Completed in {elapsed:.2f} seconds")
    print(f"Final file size: {final_size / (1024**3):.2f}GB")
    print(f"Average speed: {(final_size / (1024**2)) / elapsed:.0f} MB/s")
    print(f"Total lines: {stats['lines_written']:,}")


async def main():
    await generate_nginx_log("nginx_sample.log", 2)


if __name__ == "__main__":
    asyncio.run(main())
