import { useState, useMemo } from 'react';
export const usePagination = (items: any[], itemsPerPage: number = 10) => {
  const [currentPage, setCurrentPage] = useState(1);
  
  const totalPages = Math.ceil(items.length / itemsPerPage);
  const paginatedItems = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage;
    return items.slice(startIndex, startIndex + itemsPerPage);
  }, [items, currentPage, itemsPerPage]);
  
  return {
    currentPage,
    totalPages,
    paginatedItems,
    setCurrentPage,
    hasNextPage: currentPage < totalPages,
    hasPrevPage: currentPage > 1
  };
};