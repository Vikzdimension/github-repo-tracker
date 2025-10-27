import { useState, useEffect } from 'react';

// Hook to detect screen size
export const useScreenSize = () => {
  const [screenSize, setScreenSize] = useState({
    width: typeof window !== 'undefined' ? window.innerWidth : 1024,
    height: typeof window !== 'undefined' ? window.innerHeight : 768,
    isMobile: typeof window !== 'undefined' ? window.innerWidth <= 768 : false,
    isTablet: typeof window !== 'undefined' ? window.innerWidth > 768 && window.innerWidth <= 1024 : false,
    isDesktop: typeof window !== 'undefined' ? window.innerWidth > 1024 : true
  });

  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      const height = window.innerHeight;
      
      setScreenSize({
        width,
        height,
        isMobile: width <= 768,
        isTablet: width > 768 && width <= 1024,
        isDesktop: width > 1024
      });
    };

    window.addEventListener('resize', handleResize);
    handleResize(); // Call once to set initial state

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return screenSize;
};

// Component to conditionally render based on screen size
export const ResponsiveWrapper = ({ children, mobile, tablet, desktop, className = '' }) => {
  const { isMobile, isTablet, isDesktop } = useScreenSize();
  
  if (isMobile && mobile) return <div className={className}>{mobile}</div>;
  if (isTablet && tablet) return <div className={className}>{tablet}</div>;
  if (isDesktop && desktop) return <div className={className}>{desktop}</div>;
  
  return <div className={className}>{children}</div>;
};

// Utility function to format dates responsively
export const formatDateResponsive = (date, isMobile = false) => {
  const dateObj = new Date(date);
  
  if (isMobile) {
    return dateObj.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: '2-digit'
    });
  }
  
  return dateObj.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
};

// Utility function to truncate text responsively
export const truncateText = (text, maxLength = 50, isMobile = false) => {
  if (!text) return 'No description';
  
  const length = isMobile ? Math.floor(maxLength * 0.7) : maxLength;
  
  if (text.length <= length) return text;
  
  return `${text.substring(0, length)}...`;
};

// Utility function to format numbers responsively
export const formatNumber = (num, isMobile = false) => {
  if (!num) return '0';
  
  if (isMobile && num >= 1000) {
    if (num >= 1000000) {
      return `${(num / 1000000).toFixed(1)}M`;
    }
    return `${(num / 1000).toFixed(1)}K`;
  }
  
  return num.toLocaleString();
};