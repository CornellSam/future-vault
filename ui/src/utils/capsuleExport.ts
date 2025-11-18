export const exportCapsules = (capsules: any[]) => {
  const dataStr = JSON.stringify(capsules, null, 2);
  const dataBlob = new Blob([dataStr], { type: 'application/json' });
  const url = URL.createObjectURL(dataBlob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'capsules.json';
  link.click();
  URL.revokeObjectURL(url);
};

export const importCapsules = (file: File): Promise<any[]> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const capsules = JSON.parse(e.target?.result as string);
        resolve(capsules);
      } catch (error) {
        reject(error);
      }
    };
    reader.onerror = () => reject(reader.error);
    reader.readAsText(file);
  });
};