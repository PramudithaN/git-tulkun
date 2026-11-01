//! Collects a GitHub account's public commit/contribution history and language hex colors
//! through the GitHub CLI (`gh api graphql`), requiring only the built-in `GITHUB_TOKEN`.

use std::collections::BTreeMap;
use std::io::ErrorKind;
use std::process::Command;

use chrono::{DateTime, NaiveDate, Utc};
use serde_json::Value;

use crate::history::{AccountSnapshot, ContributionDay, rank_languages, summarize_calendar};

const ACCOUNT_QUERY: &str = r#"
query($login: String!) {
  user(login: $login) {
    databaseId
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, orderBy: {field: UPDATED_AT, direction: DESC}) {
      nodes {
        primaryLanguage {
          name
          color
        }
      }
    }
    contributionsCollection {
      contributionCalendar {
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"#;

/// Collect an `AccountSnapshot` for `login` using `gh api graphql`.
pub fn collect_account_snapshot(login: &str) -> Result<AccountSnapshot, String> {
    let output = Command::new("gh")
        .args(["api", "graphql", "-f"])
        .arg(format!("query={ACCOUNT_QUERY}"))
        .arg("-f")
        .arg(format!("login={login}"))
        .output()
        .map_err(|err| {
            if err.kind() == ErrorKind::NotFound {
                "GitHub CLI (`gh`) is not installed or not in PATH".to_owned()
            } else {
                format!("Failed to execute `gh`: {err}")
            }
        })?;

    if !output.status.success() {
        return Err(String::from_utf8_lossy(&output.stderr).trim().to_owned());
    }

    let root: Value = serde_json::from_slice(&output.stdout)
        .map_err(|err| format!("Invalid JSON from `gh api graphql`: {err}"))?;

    let user = root
        .get("data")
        .and_then(|d| d.get("user"))
        .filter(|u| !u.is_null())
        .ok_or_else(|| format!("GitHub user `{login}` not found"))?;

    let account_id = user
        .get("databaseId")
        .and_then(Value::as_u64)
        .unwrap_or(1);

    // Extract language counts and official GitHub hex colors
    let mut lang_counts: BTreeMap<String, (String, u32)> = BTreeMap::new();
    if let Some(nodes) = user
        .get("repositories")
        .and_then(|r| r.get("nodes"))
        .and_then(Value::as_array)
    {
        for node in nodes {
            if let Some(lang) = node.get("primaryLanguage").filter(|l| !l.is_null()) {
                let name = lang
                    .get("name")
                    .and_then(Value::as_str)
                    .unwrap_or("Unknown")
                    .to_owned();
                let color = lang
                    .get("color")
                    .and_then(Value::as_str)
                    .unwrap_or("#3178c6")
                    .to_owned();
                let entry = lang_counts.entry(name).or_insert((color, 0));
                entry.1 += 1;
            }
        }
    }

    // Extract contribution days
    let mut days = Vec::new();
    if let Some(weeks) = user
        .get("contributionsCollection")
        .and_then(|c| c.get("contributionCalendar"))
        .and_then(|cal| cal.get("weeks"))
        .and_then(Value::as_array)
    {
        for week in weeks {
            if let Some(c_days) = week.get("contributionDays").and_then(Value::as_array) {
                for d in c_days {
                    if let (Some(date_str), Some(count)) = (
                        d.get("date").and_then(Value::as_str),
                        d.get("contributionCount").and_then(Value::as_u64),
                    ) {
                        if let Ok(date) = NaiveDate::parse_from_str(date_str, "%Y-%m-%d") {
                            days.push(ContributionDay {
                                date,
                                count: count as u32,
                            });
                        }
                    }
                }
            }
        }
    }

    let today: NaiveDate = DateTime::<Utc>::from(std::time::SystemTime::now()).date_naive();
    let (total_contributions, monthly_contributions, current_streak, longest_streak) =
        summarize_calendar(&days, today);

    Ok(AccountSnapshot {
        login: login.to_owned(),
        account_id,
        observed_on: today,
        total_contributions,
        monthly_contributions,
        current_streak,
        longest_streak,
        languages: rank_languages(lang_counts),
    })
}
