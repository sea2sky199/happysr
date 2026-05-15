export default function Footer() {
  return (
    <footer className="hidden md:block bg-gray-800 text-gray-400 text-center py-4 text-sm">
      © {new Date().getFullYear()} HappySR — Senior Resource Center
    </footer>
  );
}
