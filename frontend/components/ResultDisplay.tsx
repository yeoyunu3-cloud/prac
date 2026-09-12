import React, { useState } from "react";

interface ResultDisplayProps {
  data: any;
  videoId: string;
  onReset: () => void;
}

export default function ResultDisplay({ data, videoId, onReset }: ResultDisplayProps) {
  const [copiedSection, setCopiedSection] = useState<string | null>(null);

  const handleCopy = (text: string, section: string) => {
    navigator.clipboard.writeText(text);
    setCopiedSection(section);
    setTimeout(() => setCopiedSection(null), 2000);
  };

  const handleDownloadMarkdown = () => {
    const markdown = generateMarkdown(data);
    const element = document.createElement("a");
    element.setAttribute("href", "data:text/markdown;charset=utf-8," + encodeURIComponent(markdown));
    element.setAttribute(
      "download",
      `${data.title.replace(/\s+/g, "_")}_${new Date().toISOString().split("T")[0]}.md`
    );
    element.style.display = "none";
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  if (!data.summary) {
    return null;
  }

  const summary = data.summary;

  return (
    <div className="w-full space-y-6">
      {/* Video Info */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="flex flex-col md:flex-row gap-6 p-6">
          {data.thumbnail_url && (
            <img
              src={data.thumbnail_url}
              alt={data.title}
              className="w-full md:w-48 h-32 md:h-auto object-cover rounded-lg"
            />
          )}
          <div className="flex-1 space-y-3">
            <div>
              <p className="text-sm text-gray-600">제목 (Title)</p>
              <h2 className="text-2xl font-bold text-gray-900">{data.title}</h2>
            </div>
            <div>
              <p className="text-sm text-gray-600">채널 (Channel)</p>
              <p className="text-lg text-gray-800">{data.channel}</p>
            </div>
            <a
              href={`https://www.youtube.com/watch?v=${videoId}`}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-2"
            >
              Watch on YouTube →
            </a>
          </div>
        </div>
      </div>

      {/* One Line Summary */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg shadow-md p-6">
        <div className="flex justify-between items-start gap-4">
          <div className="flex-1">
            <p className="text-sm text-gray-600 mb-2">한 줄 요약 (One-Line Summary)</p>
            <p className="text-lg font-semibold text-gray-900">{summary.one_line_summary}</p>
          </div>
          <button
            onClick={() => handleCopy(summary.one_line_summary, "one-line")}
            className="px-3 py-2 bg-white border border-gray-300 rounded text-sm hover:bg-gray-50 transition-colors"
            title="Copy to clipboard"
          >
            {copiedSection === "one-line" ? "✓ Copied" : "Copy"}
          </button>
        </div>
      </div>

      {/* Overview */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-3">전체 개요 (Overview)</h3>
        <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">{summary.overview}</p>
        <button
          onClick={() => handleCopy(summary.overview, "overview")}
          className="mt-4 px-3 py-2 bg-gray-100 border border-gray-300 rounded text-sm hover:bg-gray-50 transition-colors"
        >
          {copiedSection === "overview" ? "✓ Copied" : "Copy this section"}
        </button>
      </div>

      {/* Key Points */}
      {summary.key_points && summary.key_points.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">핵심 포인트 (Key Points)</h3>
          <ul className="space-y-2">
            {summary.key_points.map((point: string, idx: number) => (
              <li key={idx} className="flex gap-3 text-gray-700">
                <span className="text-indigo-600 font-bold flex-shrink-0">•</span>
                <span>{point}</span>
              </li>
            ))}
          </ul>
          <button
            onClick={() => handleCopy(summary.key_points.join("\n"), "key-points")}
            className="mt-4 px-3 py-2 bg-gray-100 border border-gray-300 rounded text-sm hover:bg-gray-50 transition-colors"
          >
            {copiedSection === "key-points" ? "✓ Copied" : "Copy this section"}
          </button>
        </div>
      )}

      {/* Chapters */}
      {summary.chapters && summary.chapters.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">챕터 (Chapters)</h3>
          <div className="space-y-3">
            {summary.chapters.map((chapter: any, idx: number) => (
              <div key={idx} className="border-l-4 border-indigo-500 pl-4 py-2">
                <a
                  href={`https://www.youtube.com/watch?v=${videoId}&t=${chapter.timestamp_seconds}s`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm font-semibold text-indigo-600 hover:text-indigo-800"
                >
                  {chapter.timestamp_label}: {chapter.title}
                </a>
                <p className="text-gray-700 mt-1">{chapter.summary}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Important Terms */}
      {summary.important_terms && summary.important_terms.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">주요 용어 (Important Terms)</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {summary.important_terms.map((term: any, idx: number) => (
              <div key={idx} className="border border-gray-200 rounded-lg p-3">
                <p className="font-bold text-gray-900">{term.term}</p>
                <p className="text-sm text-gray-700 mt-1">{term.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action Items */}
      {summary.action_items && summary.action_items.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">실천 항목 (Action Items)</h3>
          <ul className="space-y-2">
            {summary.action_items.map((item: string, idx: number) => (
              <li key={idx} className="flex gap-3 text-gray-700">
                <span className="text-green-600 font-bold flex-shrink-0">✓</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Quiz */}
      {summary.quiz && summary.quiz.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">복습 퀴즈 (Quiz)</h3>
          <div className="space-y-4">
            {summary.quiz.map((q: any, idx: number) => (
              <details key={idx} className="border border-gray-200 rounded-lg p-3">
                <summary className="cursor-pointer font-semibold text-gray-900 hover:text-indigo-600">
                  Q: {q.question}
                </summary>
                <p className="mt-3 text-gray-700 bg-gray-50 p-3 rounded">
                  <strong>A:</strong> {q.answer}
                </p>
              </details>
            ))}
          </div>
        </div>
      )}

      {/* Metadata */}
      <div className="bg-gray-50 rounded-lg p-6 text-sm">
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <div>
            <p className="text-gray-600">대상 (Target Audience)</p>
            <p className="font-semibold text-gray-900">{summary.target_audience}</p>
          </div>
          <div>
            <p className="text-gray-600">난이도 (Difficulty)</p>
            <p className="font-semibold text-gray-900">{summary.difficulty}</p>
          </div>
          <div>
            <p className="text-gray-600">원본 언어 (Transcript)</p>
            <p className="font-semibold text-gray-900">{data.transcript_language}</p>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-3">
        <button
          onClick={handleDownloadMarkdown}
          className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors"
        >
          📥 Download as Markdown
        </button>
        <button
          onClick={onReset}
          className="flex-1 bg-gray-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-gray-700 transition-colors"
        >
          ↺ Summarize Another Video
        </button>
      </div>
    </div>
  );
}

function generateMarkdown(data: any): string {
  const summary = data.summary;
  let markdown = "";

  markdown += `# ${data.title}\n\n`;
  markdown += `**Channel:** ${data.channel}\n`;
  markdown += `**Video:** https://www.youtube.com/watch?v=${data.video_id}\n\n`;

  markdown += `## 한 줄 요약\n\n${summary.one_line_summary}\n\n`;

  markdown += `## 전체 개요\n\n${summary.overview}\n\n`;

  if (summary.key_points && summary.key_points.length > 0) {
    markdown += `## 핵심 포인트\n\n`;
    summary.key_points.forEach((point: string) => {
      markdown += `- ${point}\n`;
    });
    markdown += "\n";
  }

  if (summary.chapters && summary.chapters.length > 0) {
    markdown += `## 챕터\n\n`;
    summary.chapters.forEach((chapter: any) => {
      markdown += `### ${chapter.timestamp_label}: ${chapter.title}\n\n${chapter.summary}\n\n`;
    });
  }

  if (summary.important_terms && summary.important_terms.length > 0) {
    markdown += `## 주요 용어\n\n`;
    summary.important_terms.forEach((term: any) => {
      markdown += `**${term.term}:** ${term.description}\n\n`;
    });
  }

  if (summary.action_items && summary.action_items.length > 0) {
    markdown += `## 실천 항목\n\n`;
    summary.action_items.forEach((item: string) => {
      markdown += `- ${item}\n`;
    });
    markdown += "\n";
  }

  if (summary.quiz && summary.quiz.length > 0) {
    markdown += `## 복습 퀴즈\n\n`;
    summary.quiz.forEach((q: any, idx: number) => {
      markdown += `**Q${idx + 1}: ${q.question}**\n\nA: ${q.answer}\n\n`;
    });
  }

  markdown += `---\n\n`;
  markdown += `Generated by YouTube Lecture Summarizer\n`;

  return markdown;
}
