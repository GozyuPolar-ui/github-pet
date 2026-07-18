# 🐣 GitHub Activity Pet

Pet virtual yang hidup berdasarkan aktivitas coding di GitHub. Rajin commit, pet-nya sehat & seneng. Bolong beberapa hari, pet-nya lemes. Update otomatis tiap hari lewat GitHub Actions — gak ada campur tangan manual.

![pet](assets/dog_Idle.png?t=1784338945)

## Cara Kerja

1. GitHub Actions jalan otomatis tiap hari jam 00:00 UTC
2. Script Python fetch data kontribusi setahun terakhir lewat GitHub GraphQL API
3. Berdasarkan commit hari ini & streak, sistem tentuin salah satu dari 4 state pet
4. README diupdate otomatis, nunjukin sprite sesuai state

## State Pet

| State | Kondisi | Sprite |
|---|---|---|
| 🔥 Happy | Commit hari ini + streak ≥ 3 hari | dog_happy.png |
| 🚶 Walk | Commit hari ini, streak < 3 hari | dog_Walk.png |
| 💤 Idle | Belum commit hari ini, gap < 5 hari | dog_Idle.png |
| 💀 Dead | Gak ada commit ≥ 5 hari | dog_dead.png |

## Setup Sendiri

1. Fork/clone repo ini, rename jadi `USERNAME/USERNAME` (harus sama persis dengan username GitHub kamu)
2. Bikin Personal Access Token (scope `read:user`) — Settings → Developer settings → Personal access tokens
3. Tambahin token itu sebagai repo secret dengan nama `GH_PAT` — Settings → Secrets and variables → Actions
4. Jalanin workflow manual pertama kali lewat tab **Actions** → **Update GitHub Pet** → **Run workflow**
5. Pet bakal otomatis muncul & ke-update tiap hari

## Testing Lokal

```bash
pip install requests
python scripts/update_pet.py
```
(set `GH_TOKEN` dan `GH_USERNAME` sebagai environment variable dulu sebelum run)

## Tech Stack

- Python (fetch data GitHub + update README)
- GitHub GraphQL API (data kontribusi)
- GitHub Actions (automation & scheduling)

## Struktur Project

```
github-pet/
├── assets/
│   ├── dog_happy.png
│   ├── dog_Idle.png
│   ├── dog_Walk.png
│   └── dog_dead.png
├── scripts/
│   └── update_pet.py
├── .github/workflows/
│   └── update-pet.yml
└── README.md
```