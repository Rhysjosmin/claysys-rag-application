"use client";

import { useEffect, useState } from "react";
import { Send, Loader2, FileText } from "lucide-react";
import { useDropzone } from "react-dropzone";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import { toast } from "@/hooks/use-toast";
import { cn } from "@/lib/utils";
import { CONFIG } from "@/lib/config";

interface Message {
	text: string;
	sender: "user" | "bot";
}

interface File {
	name: string;
	type: string;
}

export default function ChatInterface() {
	const [messages, setMessages] = useState<Message[]>([]);
	const [files, setFiles] = useState<File[]>([]);
	const [input, setInput] = useState("");
	const [isLoading, setIsLoading] = useState(false);
	const [isUploading, setIsUploading] = useState(false);

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		if (!input.trim() || isLoading) return;

		try {
			setIsLoading(true);
			setMessages([...messages, { text: input, sender: "user" }]);

			const response = await fetch(
				`${CONFIG.server}/query?query=${encodeURIComponent(input)}&context=${encodeURIComponent(messages.map((x) => x.text).join("---"))}`,
				{
					method: "POST",
				},
			);

			const data = await response.json();
			console.log(data);

			if (!response.ok)
				throw new Error(data.detail?.[0]?.msg || "Failed to process query");

			setMessages((prev) => [...prev, { text: data, sender: "bot" }]);
			setInput("");
		} catch (error) {
			toast({
				title: "Error",
				description:
					error instanceof Error
						? error.message
						: "Failed to send message. Please try again.",
				variant: "destructive",
			});
		} finally {
			setIsLoading(false);
		}
	};

	const onDrop = async (acceptedFiles: File[]) => {
		try {
			setIsUploading(true);

			for (const file of acceptedFiles) {
				const formData = new FormData();
				if (!(file instanceof Blob)) return;
				formData.append("file", file);

				const response = await fetch(`${CONFIG.server}/insert_doc`, {
					method: "POST",
					body: formData,
				});

				const data = await response.json();

				if (!response.ok)
					throw new Error(data.detail?.[0]?.msg || "Failed to upload document");

				setFiles((prev) => [...prev, { name: file.name, type: file.type }]);
			}

			toast({
				title: "Success",
				description: "Files uploaded successfully",
			});
		} catch (error) {
			toast({
				title: "Error",
				description:
					error instanceof Error
						? error.message
						: "Failed to upload files. Please try again.",
				variant: "destructive",
			});
		} finally {
			setIsUploading(false);
		}
	};

	const { getRootProps, getInputProps, isDragActive } = useDropzone({
		onDrop,
		accept: {
			"application/pdf": [".pdf"],
		},
		multiple: true,
	});

	useEffect(() => {
		fetch(`${CONFIG.server}/vector_docs`)
			.then((r) => r.json())
			.then((d) => {
				console.log(d);
				setFiles(
					d.map((x) => {
						return { name: x, type: "pdf" };
					}),
				);
			});
	}, []);

	return (
		<div className="flex h-full w-full mx-auto bg-white overflow-hidden">
			<div className="flex-1 flex flex-col">
				<div className="flex flex-col flex-1 p-4 overflow-y-auto space-y-4">
					{messages.map((message, i) => (
						<div
							key={i.toString() + message.sender}
							className={cn(
								message.sender === "user" ? "justify-end" : "justify-start ",
								"flex",
							)}
						>
							<div className={"max-w-[80%]  "}>{message.text}</div>
						</div>
					))}
				</div>
				<form onSubmit={handleSubmit} className="p-4 border-t">
					<div className="flex gap-2">
						<Input
							value={input}
							onChange={(e) => setInput(e.target.value)}
							placeholder="Who is the ..."
							className="flex-1"
							disabled={isLoading}
						/>
						<Button
							type="submit"
							size="icon"
							variant="ghost"
							disabled={isLoading}
						>
							{isLoading ? (
								<Loader2 className="h-4 w-4 animate-spin" />
							) : (
								<Send className="h-4 w-4" />
							)}
						</Button>
					</div>
				</form>
			</div>
			<div className="w-80 border-l bg-gray-50 flex flex-col">
				<div className="flex-1 p-4 space-y-2">
					{files.map((file, i) => (
						<div key={i} className="flex  gap-2 ">
							<FileText className="size-4" />
							<div className=" text-sm text-black/65 flex-1 max-h-8 text-ellipsis overflow-hidden truncate">
								{file.name}
							</div>
						</div>
					))}
				</div>
				<div
					{...getRootProps()}
					className={`h-32 m-4 rounded-lg border-2 border-dashed 
            ${isDragActive ? "border-primary bg-primary/10" : "border-gray-300"} 
            flex flex-col items-center justify-center text-gray-500 transition-colors
            ${isUploading ? "opacity-50 cursor-not-allowed" : "cursor-pointer"}`}
				>
					<input {...getInputProps()} disabled={isUploading} />
					{isUploading ? (
						<>
							<Loader2 className="h-6 w-6 animate-spin" />
							<p className="mt-2 text-sm">Uploading...</p>
						</>
					) : isDragActive ? (
						<p>Drop the files here...</p>
					) : (
						<p>Drop any files here</p>
					)}
				</div>
			</div>
		</div>
	);
}

