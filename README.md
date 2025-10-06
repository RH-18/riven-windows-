<div align="center">
  <a href="https://github.com/rivenmedia/riven">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/rivenmedia/riven/main/assets/riven-light.png">
      <img alt="riven" src="https://raw.githubusercontent.com/rivenmedia/riven/main/assets/riven-dark.png">
    </picture>
  </a>
</div>

<div align="center">
  <a href="https://github.com/rivenmedia/riven/stargazers"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/rivenmedia/riven"></a>
  <a href="https://github.com/rivenmedia/riven/issues"><img alt="Issues" src="https://img.shields.io/github/issues/rivenmedia/riven" /></a>
  <a href="https://github.com/rivenmedia/riven/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/rivenmedia/riven"></a>
  <a href="https://github.com/rivenmedia/riven/graphs/contributors"><img alt="Contributors" src="https://img.shields.io/github/contributors/rivenmedia/riven" /></a>
  <a href="https://discord.gg/rivenmedia"><img alt="Discord" src="https://img.shields.io/badge/Join%20discord-8A2BE2" /></a>
</div>

<div align="center">
  <p>Plex torrent streaming through Debrid and 3rd party services like Overseerr, Mdblist, etc.</p>
</div>

Services currently supported:

| Type              | Supported                                                                         |
| ----------------- | --------------------------------------------------------------------------------- |
| Debrid services   | Real Debrid, All Debrid, TorBox                                                   |
| Content services  | Plex Watchlist, Overseerr, Mdblist, Listrr, Trakt                                 |
| Scraping services | Comet, Jackett, Torrentio, Orionoid, Mediafusion, Prowlarr, Zilean, Rarbg         |
| Media servers     | Plex, Jellyfin, Emby                                                              |

and more to come!

Check out out [Project Board](https://github.com/users/dreulavelle/projects/2) to stay informed!

Please add feature requests and issues over on our [Issue Tracker](https://github.com/rivenmedia/riven/issues) or join our [Discord](https://discord.gg/rivenmedia) to chat with us!

We are constantly adding features and improvements as we go along and squashing bugs as they arise.

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [ElfHosted](#elfhosted)
- [Native Windows Setup](#native-windows-setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Backend](#running-the-backend)
  - [Running the Frontend](#running-the-frontend)
  - [Plex Libraries](#plex-libraries)
  - [Troubleshooting](#troubleshooting)
- [RivenVFS and Caching](#rivenvfs-and-caching)
- [Development](#development)
  - [Clone and Bootstrap](#clone-and-bootstrap)
  - [Running the Backend Manually](#running-the-backend-manually)
  - [Running Tests](#running-tests)
  - [Additional Tips](#additional-tips)
- [Contributing](#contributing)
  - [Submitting Changes](#submitting-changes)
  - [Code Formatting](#code-formatting)
  - [Dependency Management](#dependency-management)
    - [Adding or Updating Dependencies](#adding-or-updating-dependencies)
  - [Running Tests and Linters](#running-tests-and-linters)
- [License](#license)

---

## ElfHosted

[ElfHosted](https://elfhosted.com) is a geeky [open-source](https://elfhosted.com/open/) PaaS which provides all the "plumbing" (_hosting, security, updates, etc_) for your self-hosted apps.

> [!IMPORTANT]
> **ElfHosted ❤️ Riven 100%**
> [Riven](https://elfhosted.com/app/riven/) is an "Elf-icial" app in the [ElfHosted app catalogue](https://elfhosted.com/apps/) - A whopping :heart_eyes_cat::heart_eyes_cat: 100% :heart_eyes_cat::heart_eyes_cat: of your subscription goes directly to Riven developers, who can usually be found in the [#elf-riven](https://discord.com/channels/396055506072109067/1253110932062601276) channel in the [ElfHosted Discord Server](https://discord.elfhosted.com).

Curious how it works? Here's an [explainer video](https://www.youtube.com/watch?v=ZHZAEhLuJqk)!

> [!TIP]
> **ElfHosted "Infinite Streaming" bundles**
> Riven is pre-packaged with Plex, Zurg, and symlinks, and ready-to-go, in these convenient bundles:
>
> -   [Starter Kit](https://store.elfhosted.com/product/plex-riven-infinite-streaming-starter-kit) (_quick and easy setup_)
> -   [Hobbit Bundle](https://store.elfhosted.com/product/hobbit-riven-real-debrid-infinite-streaming-bundle) (_12.5% dedicated node, with extras_)
> -   [Ranger Bundle](https://store.elfhosted.com/product/plex-riven-infinite-streaming-plus-bundle) (_25% dedicated node, with extras_)

## Native Windows Setup

### Prerequisites

- Windows 11 with the latest updates.
- PowerShell 5.1 or PowerShell 7 (all examples below use PowerShell syntax).
- [Python 3.11+ for Windows](https://www.python.org/downloads/windows/) with **Add python.exe to PATH** enabled during installation.
- [Git for Windows](https://git-scm.com/download/win).
- Optional: [Node.js 18+](https://nodejs.org/) when you plan to work on the standalone frontend.
- Optional: Plex Media Server for Windows if you want to integrate with Plex locally.

### Installation

1. Decide where you want Riven to keep its data. The examples below assume `C:\Riven`, but you can substitute any writable location.
2. Create the directories Riven expects by running the following in PowerShell:

   ```powershell
   $root = 'C:\Riven'
   New-Item -ItemType Directory -Force -Path $root, (Join-Path $root 'mount'), (Join-Path $root 'data') | Out-Null
   ```

3. Clone the repository and switch into it:

   ```powershell
   git clone https://github.com/rivenmedia/riven.git
   Set-Location riven
   ```

4. Allow scripts for the current session (if you have not already) and launch the backend bootstrapper:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\scripts\Start-Backend.ps1 -IncludeDevDependencies
   ```

   The script provisions a `.venv` directory, installs Poetry, restores dependencies (including the optional developer extras when `-IncludeDevDependencies` is supplied), and starts the FastAPI backend on port `8080`. Press <kbd>Ctrl</kbd>+<kbd>C</kbd> to stop it when you are finished.

5. In the Riven web UI, set the Filesystem mount path to the directory you created earlier (for example `C:\Riven\mount`). Any folders you create under that mount path (`movies`, `shows`, and so on) will be exposed to Plex and other media servers.

### Running the Backend

Whenever you want to bring Riven online, open PowerShell in the repository root and run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
./scripts/Start-Backend.ps1
```

Use `-Port <number>` to choose a different listening port, `-SkipInstall` when you only want to reuse the existing virtual environment, and `-EnableDebugger` to opt into extra debugging output.

### Running the Frontend

The backend bundles the settings UI, but you can also run the standalone frontend when you want hot reloading or to work on UI changes. After cloning the UI repository next to this one (for example `C:\Riven\frontend`), run:

```powershell
./scripts/Start-Frontend.ps1 -FrontendPath ..\frontend
```

The script picks `npm` by default. Override it with `-PackageManager pnpm`, `-PackageManager yarn`, or `-PackageManager bun` if you use an alternative toolchain. Forward additional CLI flags with `-ScriptArguments "-- --host localhost --port 3000"`.

### Plex Libraries

Create the library folders you want Plex to index beneath your chosen mount directory. Riven expects the following sections to exist:

| Type   | Categories               |
| ------ | ------------------------ |
| Movies | `movies`, `anime_movies` |
| Shows  | `shows`, `anime_shows`   |

Point Plex at the same Windows paths that Riven uses (for example `C:\Riven\mount\movies`). Keeping the paths identical between Riven and Plex avoids sync issues.

### Troubleshooting

- **Riven UI cannot see your media folders:** Confirm the path in *Settings → Filesystem* matches the directory you created earlier (for example `C:\Riven\mount`). Use `Test-Path 'C:\Riven\mount'` in PowerShell to verify it exists.
- **Plex does not detect new files:** Make sure Plex is pointed at the exact same Windows path as Riven and that your Windows account has permission to read the folders. Trigger a library refresh from Plex after the first sync.
- **Need a clean restart:** Close the PowerShell window running Riven or press <kbd>Ctrl</kbd>+<kbd>C</kbd>, then rerun `./scripts/Start-Backend.ps1`.

## RivenVFS and Caching

### What the settings do
- `cache_dir`: Directory to store on‑disk cache files (use a user‑writable path).
- `cache_max_size_mb`: Max cache size (MB) for the VFS cache directory.
- `chunk_size_mb`: Size of individual CDN requests (MB). Default 32MB provides good balance between efficiency and connection reliability.
- `fetch_ahead_chunks`: Number of chunks to prefetch ahead of current read position. Default 4 chunks prefetches 128MB ahead (4 × 32MB) for smooth streaming with fair multi-user scheduling.
- `ttl_seconds`: Optional expiry horizon when using `eviction = "TTL"` (default eviction is `LRU`).

- Eviction behavior:
  - LRU (default): Strictly enforces the configured size caps by evicting least‑recently‑used blocks when space is needed.
  - TTL: First removes entries that have been idle longer than `ttl_seconds` (sliding expiration). If the cache still exceeds the configured size cap after TTL pruning, it additionally trims oldest entries (LRU) until usage is within the limit.

## Development

Welcome to the development section! Here, you'll find the steps required to set up a native Windows environment and start contributing to the project.

### Clone and Bootstrap

1. **Clone the Repository**

   ```powershell
   git clone https://github.com/rivenmedia/riven.git
   Set-Location riven
   ```

2. **Provision the Virtual Environment**

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ./scripts/Start-Backend.ps1 -IncludeDevDependencies
   ```

   Running the script once sets up the `.venv` directory, installs Poetry, restores dependencies (including the developer extras), and starts the backend. Use <kbd>Ctrl</kbd>+<kbd>C</kbd> to stop it after the install completes.

### Running the Backend Manually

After the initial bootstrap you can control the backend directly from PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
poetry run python src/main.py --port 8080
deactivate
```

Adjust the `--port` argument as needed. Activating the virtual environment first ensures `poetry` and the project dependencies resolve correctly.

### Running Tests

Activate the virtual environment and invoke the test suite through Poetry:

```powershell
.\.venv\Scripts\Activate.ps1
poetry run pytest
deactivate
```

Pass additional arguments (for example `poetry run pytest src/tests/test_updaters.py`) to narrow the scope during development.

### Additional Tips

- **Environment Variables:** Set the `ORIGIN` environment variable to the URL where the frontend will be accessible.

  ```powershell
  $Env:ORIGIN = 'http://localhost:3000'
  ```

- **Dependency Tweaks:** Re-run `./scripts/Start-Backend.ps1 -IncludeDevDependencies` after modifying `pyproject.toml` to make sure the lock file and virtual environment stay in sync.
- **Frontend Workflows:** Use `./scripts/Start-Frontend.ps1` for hot reloading and pass `-ScriptArguments` to forward flags directly to the underlying package manager.

## Contributing

We welcome contributions from the community! To ensure a smooth collaboration, please follow these guidelines:

### Submitting Changes

1. **Open an Issue**: For major changes, start by opening an issue to discuss your proposed modifications. This helps us understand your intentions and provide feedback early in the process.
2. **Pull Requests**: Once your changes are ready, submit a pull request. Ensure your code adheres to our coding standards and passes all tests. Commits should follow [conventional-commits](https://www.conventionalcommits.org/) specification.

### Code Formatting

-   We use [Black](https://black.readthedocs.io/en/stable/) for code formatting. Run `black` on your code before submitting.
-   Use CRLF line endings unless the file is a shell script or another format that requires LF line endings.

### Dependency Management

We use [Poetry](https://python-poetry.org/) for managing dependencies. Poetry simplifies dependency management by automatically handling package versions and resolving conflicts, ensuring consistency across all environments.

#### Adding or Updating Dependencies

-   **Add a Dependency**: Use `poetry add <package-name>` to add a new dependency.
-   **Update a Dependency**: Use `poetry update <package-name>` to update an existing dependency.

### Running Tests and Linters

Before submitting a pull request, ensure your changes are compatible with the project's dependencies and coding standards. Use the following commands to run tests and linters:

-   **Run Tests**: `poetry run pytest`
-   **Run Linters**: `poetry run ruff check backend` and `poetry run isort --check-only backend`

By following these guidelines, you help us maintain a high-quality codebase and streamline the review process. Thank you for contributing!

---

<a href="https://github.com/rivenmedia/riven/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=rivenmedia/riven" />
</a>

---

<div align="center">
  <h1>Riven Analytics</h1>
  <img alt="Alt" src="https://repobeats.axiom.co/api/embed/9a780bcd591b50aa26de6b8226b1de938bde5adb.svg" title="Repobeats analytics image">
</div>

## License

This project is licensed under the GNU GPLv3 License - see the [LICENSE](LICENSE) file for details
