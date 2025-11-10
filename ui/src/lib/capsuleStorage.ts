export const saveCapsule = (data: any) => localStorage.setItem("capsule", JSON.stringify(data));
export const getCapsule = () => JSON.parse(localStorage.getItem("capsule") || "{}");