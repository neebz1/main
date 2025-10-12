# 🌟 Top GitHub Repositories Finder

Discover the most popular and influential GitHub repositories with this easy-to-use tool!

## 🚀 Quick Start

### Easiest Way (No Setup Required):
```bash
./show-top-github-repos.sh
```

This shows the top 20 most popular GitHub repositories based on stars.

---

## 📋 Features

✅ **Find top repositories** by stars, forks, or recent updates  
✅ **Filter by language** (Python, JavaScript, Go, etc.)  
✅ **Offline mode** - No API rate limits, instant results  
✅ **Detailed information** - Stars, forks, description, language  
✅ **Beautiful formatting** - Easy to read output  

---

## 💡 Usage Examples

### Show Top 20 Repositories:
```bash
./show-top-github-repos.sh
```

### Show Top 10 Repositories:
```bash
./show-top-github-repos.sh -c 10
```

### Filter by Language:
```bash
# Top 10 Python repositories
./show-top-github-repos.sh -c 10 -l python

# Top 15 JavaScript repositories
./show-top-github-repos.sh -c 15 -l javascript

# Top 20 Rust repositories
./show-top-github-repos.sh -c 20 -l rust
```

### Show Detailed Information:
```bash
./show-top-github-repos.sh -d
```

### Direct Python Usage:
```bash
# Offline mode (recommended - no rate limits)
python3 top20_github_repos.py --offline

# Live API mode (requires GitHub token for higher limits)
export GITHUB_TOKEN="your_github_token_here"
python3 top20_github_repos.py -c 30 -l python

# Sort by forks instead of stars
python3 top20_github_repos.py --offline -s forks
```

---

## 🎯 Common Use Cases

### 1. **Discover Popular Projects**
Find trending repositories in your favorite language:
```bash
./show-top-github-repos.sh -l typescript -c 15
```

### 2. **Learn from the Best**
See what the most successful projects are using:
```bash
./show-top-github-repos.sh -d
```

### 3. **Find Learning Resources**
Many top repos are educational resources:
```bash
./show-top-github-repos.sh -c 30
```

### 4. **Research Tech Stacks**
See what languages and frameworks are most popular:
```bash
./show-top-github-repos.sh -l go
```

---

## 📊 What You'll See

For each repository, you get:
- **Repository name** (e.g., `facebook/react`)
- **⭐ Stars** - How many people starred it
- **🍴 Forks** - How many times it's been forked
- **💻 Language** - Primary programming language
- **📝 Description** - What the project does
- **🔗 URL** - Direct link to the repository

### Detailed Mode (with `-d` flag) also shows:
- Open issues count
- Watchers count
- Creation date
- Last update date

---

## 🔧 Advanced Options

```bash
# Show help
python3 top20_github_repos.py --help

# Custom count (any number)
python3 top20_github_repos.py --offline -c 50

# Sort by different criteria
python3 top20_github_repos.py --offline -s forks  # By forks
python3 top20_github_repos.py -s updated          # By recent updates (needs API)

# Combine filters
python3 top20_github_repos.py --offline -c 15 -l javascript -d
```

---

## 🌐 API vs Offline Mode

### Offline Mode (Default with launcher):
- ✅ **No rate limits** - Use as much as you want
- ✅ **Instant results** - No API calls needed
- ✅ **Curated list** - Top 20 most popular repos
- ⚠️ **Static data** - Not real-time

### API Mode:
- ✅ **Real-time data** - Fresh from GitHub
- ✅ **More options** - Sort by updates, more filters
- ✅ **Unlimited repos** - Get as many as you need
- ⚠️ **Rate limits** - 60 requests/hour without token
- ⚠️ **Requires token** - Set `GITHUB_TOKEN` for higher limits

To use API mode, remove the `--offline` flag:
```bash
python3 top20_github_repos.py -c 30 -l python
```

---

## 🔑 GitHub Token (Optional)

For API mode with higher rate limits:

1. **Create a token**: https://github.com/settings/tokens
2. **Set environment variable**:
   ```bash
   export GITHUB_TOKEN="your_token_here"
   ```
3. **Use the tool** without rate limits!

---

## 📚 Supported Languages

You can filter by any programming language, including:
- `python`
- `javascript`
- `typescript`
- `go`
- `rust`
- `java`
- `c++`
- `c`
- `ruby`
- `php`
- `swift`
- `kotlin`
- `dart`
- `shell`
- And many more!

---

## 🎨 Example Output

```
================================================================================
                     🌟 TOP 5 GITHUB REPOSITORIES 🌟
================================================================================

1. freeCodeCamp/freeCodeCamp
   ⭐ Stars: 400,000 | 🍴 Forks: 37,000 | 💻 Language: TypeScript
   📝 freeCodeCamp.org's open-source codebase and curriculum. Learn to code for free.
   🔗 https://github.com/freeCodeCamp/freeCodeCamp

2. facebook/react
   ⭐ Stars: 228,000 | 🍴 Forks: 46,000 | 💻 Language: JavaScript
   📝 The library for web and native user interfaces
   🔗 https://github.com/facebook/react

...
```

---

## 🆘 Troubleshooting

### Error: "403 Forbidden"
You've hit GitHub's API rate limit. Solutions:
1. Use offline mode: `./show-top-github-repos.sh` (default)
2. Wait an hour and try again
3. Set a GitHub token (see above)

### Error: "requests module not found"
Install dependencies:
```bash
pip3 install requests
```

---

## 💡 Tips

1. **Use offline mode** for quick lookups without rate limits
2. **Combine filters** to find exactly what you're looking for
3. **Use detailed mode** (`-d`) to get more insights
4. **Explore different languages** to discover new technologies
5. **Save results** by redirecting output: `./show-top-github-repos.sh > repos.txt`

---

## 🔗 Integration with Other Tools

This tool works great alongside:
- **Cursor AI** - Ask AI about repositories you find
- **Logic Pro Copilot** - Find music production repos
- **Cloud AI Builder** - Clone and customize repos

---

## 📊 Statistics

The curated offline list includes:
- **20 top repositories** across multiple languages
- Combined **3+ million stars**
- Repositories from major tech companies and communities
- Diverse languages: JavaScript, Python, Rust, Go, C++, TypeScript, and more

---

**🚀 Start exploring now!**
```bash
./show-top-github-repos.sh
```

Happy coding! 🎉
