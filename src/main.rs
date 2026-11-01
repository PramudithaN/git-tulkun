//! CLI entrypoint for `git-tulkun`.
//!
//! Commands:
//! - `git-tulkun collect <login> [--output snapshot.json]`
//! - `git-tulkun render <snapshot.json> [--output-dir tulkun] [--view side|dive|top] [--canon]`
//! - `git-tulkun demo [--commits 140] [--output-dir tulkun] [--view side|dive|top]`

use std::env;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::ExitCode;

use chrono::NaiveDate;
use git_tulkun::coat::TulkunCoat;
use git_tulkun::collect::collect_account_snapshot;
use git_tulkun::history::{AccountSnapshot, LanguageShare};
use git_tulkun::output::{encode_gif, encode_png, encode_preview_html};
use git_tulkun::render::{
    CameraView, LOOP_FRAME_COUNT, TulkunBiology, TulkunFrame, render_still_frame,
    render_swim_frame,
};

fn main() -> ExitCode {
    let args: Vec<String> = env::args().skip(1).collect();
    match run_cli(&args) {
        Ok(()) => ExitCode::SUCCESS,
        Err(err) => {
            eprintln!("git-tulkun: {err}");
            ExitCode::FAILURE
        }
    }
}

fn run_cli(args: &[String]) -> Result<(), String> {
    let Some(subcommand) = args.first().map(String::as_str) else {
        return Err(usage_text());
    };

    match subcommand {
        "collect" => {
            let login = args
                .get(1)
                .ok_or_else(|| "missing <login> for `collect`".to_owned())?;
            let mut output_path: Option<PathBuf> = None;
            let mut i = 2;
            while i < args.len() {
                match args[i].as_str() {
                    "--output" | "-o" => {
                        let p = args.get(i + 1).ok_or("missing path after --output")?;
                        output_path = Some(PathBuf::from(p));
                        i += 2;
                    }
                    other => return Err(format!("unknown option `{other}`")),
                }
            }
            let snapshot = collect_account_snapshot(login)?;
            let json = serde_json::to_string_pretty(&snapshot).map_err(|e| e.to_string())?;
            if let Some(path) = output_path {
                fs::write(&path, format!("{json}\n"))
                    .map_err(|e| format!("{}: {e}", path.display()))?;
                println!("Saved account snapshot for @{login} to {}", path.display());
            } else {
                println!("{json}");
            }
            Ok(())
        }
        "render" => {
            let snapshot_file = args
                .get(1)
                .ok_or_else(|| "missing <snapshot.json> for `render`".to_owned())?;
            let mut output_dir = PathBuf::from("tulkun");
            let mut view = CameraView::Side;
            let mut canon_only = false;

            let mut i = 2;
            while i < args.len() {
                match args[i].as_str() {
                    "--output-dir" | "-o" => {
                        let p = args.get(i + 1).ok_or("missing dir after --output-dir")?;
                        output_dir = PathBuf::from(p);
                        i += 2;
                    }
                    "--view" => {
                        let v = args.get(i + 1).ok_or("missing view after --view")?;
                        view = parse_view(v)?;
                        i += 2;
                    }
                    "--canon" => {
                        canon_only = true;
                        i += 1;
                    }
                    other => return Err(format!("unknown option `{other}`")),
                }
            }

            let raw = fs::read_to_string(snapshot_file)
                .map_err(|e| format!("{snapshot_file}: {e}"))?;
            let snapshot: AccountSnapshot =
                serde_json::from_str(&raw).map_err(|e| format!("{snapshot_file}: {e}"))?;
            render_to_directory(&snapshot, &output_dir, view, canon_only)
        }
        "demo" => {
            let mut commits = 140_u64;
            let mut output_dir = PathBuf::from("tulkun");
            let mut view = CameraView::Side;
            let mut canon_only = false;

            let mut i = 1;
            while i < args.len() {
                match args[i].as_str() {
                    "--commits" | "-c" => {
                        let c = args.get(i + 1).ok_or("missing number after --commits")?;
                        commits = c.parse::<u64>().map_err(|_| "invalid commit count")?;
                        i += 2;
                    }
                    "--output-dir" | "-o" => {
                        let p = args.get(i + 1).ok_or("missing dir after --output-dir")?;
                        output_dir = PathBuf::from(p);
                        i += 2;
                    }
                    "--view" => {
                        let v = args.get(i + 1).ok_or("missing view after --view")?;
                        view = parse_view(v)?;
                        i += 2;
                    }
                    "--canon" => {
                        canon_only = true;
                        i += 1;
                    }
                    other => return Err(format!("unknown option `{other}`")),
                }
            }

            let demo_snapshot = AccountSnapshot {
                login: "demo-user".to_owned(),
                account_id: 42,
                observed_on: NaiveDate::from_ymd_opt(2026, 11, 1).unwrap(),
                total_contributions: commits,
                monthly_contributions: commits,
                current_streak: 14,
                longest_streak: 30,
                languages: vec![
                    LanguageShare {
                        name: "TypeScript".to_owned(),
                        hex_color: "#3178c6".to_owned(),
                        repo_count: 10,
                    },
                    LanguageShare {
                        name: "Rust".to_owned(),
                        hex_color: "#dea584".to_owned(),
                        repo_count: 8,
                    },
                    LanguageShare {
                        name: "Python".to_owned(),
                        hex_color: "#3572A5".to_owned(),
                        repo_count: 5,
                    },
                ],
            };
            render_to_directory(&demo_snapshot, &output_dir, view, canon_only)
        }
        _ => Err(usage_text()),
    }
}

fn parse_view(s: &str) -> Result<CameraView, String> {
    match s.to_lowercase().as_str() {
        "side" => Ok(CameraView::Side),
        "dive" => Ok(CameraView::Dive),
        "top" => Ok(CameraView::Top),
        _ => Err(format!("unknown view `{s}` (expected `side`, `dive`, or `top`)")),
    }
}

fn render_to_directory(
    snapshot: &AccountSnapshot,
    output_dir: &Path,
    view: CameraView,
    canon_only: bool,
) -> Result<(), String> {
    let coat = TulkunCoat::from_snapshot(snapshot, canon_only);
    let swim_frames: Vec<TulkunFrame> = (0..LOOP_FRAME_COUNT)
        .map(|f| render_swim_frame(snapshot, &coat, view, f))
        .collect();

    let gif_bytes = encode_gif(&swim_frames)?;
    let png_bytes = encode_png(&render_still_frame(snapshot, &coat, view))?;

    let bio = TulkunBiology::from_commits(
        snapshot
            .total_contributions
            .max(snapshot.monthly_contributions)
            .max(1),
    );
    let caption = format!(
        "@{} — {} ({} commits)",
        snapshot.login,
        bio.stage_name(),
        bio.commits
    );
    let preview_html = encode_preview_html(&caption);

    fs::create_dir_all(output_dir).map_err(|e| format!("{}: {e}", output_dir.display()))?;
    let gif_path = output_dir.join("tulkun.gif");
    let png_path = output_dir.join("tulkun.png");
    let html_path = output_dir.join("preview.html");

    fs::write(&gif_path, gif_bytes).map_err(|e| format!("{}: {e}", gif_path.display()))?;
    fs::write(&png_path, png_bytes).map_err(|e| format!("{}: {e}", png_path.display()))?;
    fs::write(&html_path, preview_html.as_bytes())
        .map_err(|e| format!("{}: {e}", html_path.display()))?;

    println!(
        "{caption}: wrote {}, {}, {}",
        gif_path.display(),
        png_path.display(),
        html_path.display()
    );
    Ok(())
}

fn usage_text() -> String {
    "Usage:\n  \
     git-tulkun collect <login> [--output snapshot.json]\n  \
     git-tulkun render <snapshot.json> [--output-dir tulkun] [--view side|dive|top] [--canon]\n  \
     git-tulkun demo [--commits 140] [--output-dir tulkun] [--view side|dive|top] [--canon]"
        .to_owned()
}
