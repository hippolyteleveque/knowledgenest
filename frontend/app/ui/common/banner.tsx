type KnBannerProps = {
  message: string;
};

export default function KnBanner(props: KnBannerProps) {
  return (
    <div
      className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative mb-4"
      role="alert"
    >
      <span className="block sm:inline">{props.message}</span>
    </div>
  );
}
