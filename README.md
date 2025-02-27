![](https://img.shields.io/badge/状態-リリース-blue)
![](https://img.shields.io/badge/YAMANASHI_AIハッカソン-2024_最優秀賞-yellow)
![](https://img.shields.io/badge/build-passing-green)


## プロジェクト名

やまなしNavi（B.E.）

<!-- プロジェクトについて -->

## プロジェクトについて

山梨で楽しく過ごすためのAIエージェント（バックエンド）

  <p align="left">
    <br />
    <a href="https://qiita.com/Integral-07/items/be2fdeb59b07168a2c95"><strong>ハッカソン参加録（Qiita記事） »</strong></a>
    <br />
    <br />
    
### 背景
１．観光入込客数と観光消費額は”観光客数”・”消費額”の観点からコロナ禍から大きな回復基調<br>
２．山梨県は、圧倒的な地理的優位性（都市圏に近い）、観光資源（自然系、食事系）、インフラ（中央道、JRなど）が揃う希少な地域<br>
３．観光は国策への流れと後押し、2030年には訪日外国人6,000万人、消費額15兆、GDP10%の予想<br>
  
　この流れに乗って、もっと山梨観光を楽しんで欲しい！という想いで開発を始めた<br>
<p align="left">
    　<a href="https://www.pref.yamanashi.jp/documents/2062/03houkokusho2023.pdf"><strong>令和5年山梨県観光入込客統計調査報告書 »</strong></a>
    <br>
    <br>
</p>

### 概要
➢ 山梨の観光の魅力を伝える情報提供アプリ<br>
➢ ユーザーの質問、状況にもとづいて観光の提案をする<br>
➢ 会話が楽しくなるような面白さ、親しみやすさ(AIの口調やキャラ付け)<br>

### 機能
➢ 対話形式のチャットボット（というよりもエージェント）<br>
➢ 位置、移動手段、季節、やりたいこと（行く、食、遊ぶ）などにもとづき候補となるスポットの提案をする<br>
➢ ユーザーの求めに応じて、スポットについての詳細な説明をしたり、天気などのアドバイスもできる<br>

## AIプラットフォーム選定
以下の特徴を持つDifyを採用

- LLMモデル（ OpenAIの適切なモデル）
- RAG（山梨の観光スポットに関する情報を中心にKnowledgeを与える）
- APIによるアクション（モデルによる判断でAPIで外部機能を使用）
  - Goolge Search
  - Wikipedia
  - Open weather or Google
 
## フロントエンド
- Dify提供のWebサイト
- Dify提供のエンジンをHTML埋め込み
- オリジナルWebフロントエンド( https://github.com/Integral-07/YamanashiNavi_frontend )【未完成】
- LINE接続（LINE MessagingAPI）
- WhatsApp接続（未実装）

![スクリーンショット 2025-02-27 112803](https://github.com/user-attachments/assets/149896fd-9fc3-4bed-9af0-c5b487e30682)
![スクリーンショット 2025-02-27 113350](https://github.com/user-attachments/assets/2e16e4ab-79fb-41ef-910f-42ef033f6852)

## 技術スタック
![スクリーンショット 2025-02-27 113722](https://github.com/user-attachments/assets/003dafa0-1e70-4a54-bdd5-4e941ba7557d)



## 使用技術一覧

<!-- シールド一覧 -->
<p style="display: inline">
  <!-- フロントエンドのフレームワーク -->
  <img src="https://img.shields.io/badge/-LINE MessagingAPI-C0C300.svg?logo=line&style=for-the-badge">
  <!-- バックエンドのフレームワーク -->
  <img src="https://img.shields.io/badge/-Django-092E20.svg?logo=django&style=for-the-badge">
  <!-- バックエンドの言語 -->
  <img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">
  <!-- ミドルウェア -->
  <img src="https://img.shields.io/badge/-SQLite-336791.svg?logo=sqlite&style=for-the-badge">
  <!-- インフラ -->
  <img src="https://img.shields.io/badge/-Docker-1488C6.svg?logo=docker&style=for-the-badge">
  <img src="https://img.shields.io/badge/-Github-181717.svg?logo=github&style=for-the-badge">
</p>

## 環境

| 言語・フレームワーク    | バージョン  |
| --------------------- | ---------- |
| Python                | mcr.microsoft.com/devcontainers/python:1-3.12-bullseye     |
| Django                | 4.2.0      |
| sqlite                | 3.45.3     |

その他のパッケージのバージョンは requirements.lock を参照してください

