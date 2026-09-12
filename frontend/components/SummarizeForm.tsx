import React, { useState, useCallback } from "react";
import axios from "axios";
import { API_ENDPOINTS } from "@/lib/api";

export type DetailLevel = "short" | "normal" | "detailed";

interface SummarizeFormProps {
  videoId: string;
  videoTitle: string;
  availableLanguages: string[];
  onSummarizing: (summarizing: boolean) => void;
  onError: (error: string) => void;
  onSuccess: (data: any) => void;
}

export default function SummarizeForm({
  videoId,
  videoTitle,
  availableLanguages,
  onSummarizing,
  onError,
  onSuccess,
}: SummarizeFormProps) {
  const [transcriptLanguage, setTranscriptLanguage] = useState("ko");
  const [outputLanguage, setOutputLanguage] = useState("ko");
  const [detailLevel, setDetailLevel] = useState<DetailLevel>("normal");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      onError("");
      setIsSubmitting(true);
      onSummarizing(true);

      try {
        const response = await axios.post(API_ENDPOINTS.SUMMARIZE, {
          url: `https://www.youtube.com/watch?v=${videoId}`,
          transcript_language: transcriptLanguage,
          output_language: outputLanguage,
          detail_level: detailLevel,
        });

        onSuccess(response.data);
      } catch (err: any) {
        const errorMessage =
          err.response?.data?.detail || "Failed to summarize video";
        onError(errorMessage);
      } finally {
        setIsSubmitting(false);
        onSummarizing(false);
      }
    },
    [videoId, transcriptLanguage, outputLanguage, detailLevel, onSummarizing, onError, onSuccess]
  );

  const languageOptions = [
    { code: "ko", name: "한국어 (Korean)" },
    { code: "en", name: "English" },
    { code: "ja", name: "日本語 (Japanese)" },
    { code: "zh", name: "中文 (Chinese)" },
  ];

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Transcript Language */}
        <div>
          <label htmlFor="transcript-lang" className="block text-sm font-medium text-gray-700 mb-2">
            Transcript Language
          </label>
          <select
            id="transcript-lang"
            value={transcriptLanguage}
            onChange={(e) => setTranscriptLanguage(e.target.value)}
            disabled={isSubmitting}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          >
            {languageOptions.map((lang) => (
              <option key={lang.code} value={lang.code}>
                {lang.name}
              </option>
            ))}
          </select>
        </div>

        {/* Output Language */}
        <div>
          <label htmlFor="output-lang" className="block text-sm font-medium text-gray-700 mb-2">
            Output Language
          </label>
          <select
            id="output-lang"
            value={outputLanguage}
            onChange={(e) => setOutputLanguage(e.target.value)}
            disabled={isSubmitting}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          >
            {languageOptions.map((lang) => (
              <option key={lang.code} value={lang.code}>
                {lang.name}
              </option>
            ))}
          </select>
        </div>

        {/* Detail Level */}
        <div>
          <label htmlFor="detail-level" className="block text-sm font-medium text-gray-700 mb-2">
            Summary Detail
          </label>
          <select
            id="detail-level"
            value={detailLevel}
            onChange={(e) => setDetailLevel(e.target.value as DetailLevel)}
            disabled={isSubmitting}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          >
            <option value="short">짧게 (Short)</option>
            <option value="normal">보통 (Normal)</option>
            <option value="detailed">자세히 (Detailed)</option>
          </select>
        </div>
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full bg-green-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {isSubmitting ? "Summarizing... (This may take a minute)" : "Summarize"}
      </button>
    </form>
  );
}
