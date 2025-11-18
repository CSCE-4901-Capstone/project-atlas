import { useEffect } from "react";

export default function ArticleList({ articles, onClose }) {
  // Close popup when clicking outside the container
  useEffect(() => {
    function handleClick(e) {
      if (!e.target.closest(".article-pop-up")) {
        onClose();
      }
    }

    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, [onClose]);

  return (
    <div className="article-pop-up-overlay">
      <div className="article-pop-up">
        <h2>Articles</h2>
        <ol>
          {articles.map((article, idx) => (
            <li key={idx}>
              <a
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
              >
                {article.title}
              </a>
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}
