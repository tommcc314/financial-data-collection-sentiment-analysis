#include <iostream>
#include <curl/curl.h>
#include <fstream>
#include <vector>

//contains the full html of the webpage 
static std::string HTMLcontent;

// curl helper function
size_t writeRes(char* contents, size_t size, size_t nmemb, void* userp)
{
	((std::string*)userp)->append((char*)contents, size * nmemb);
	return size * nmemb;
}
//quick function to convert a tag to is corresponding closed varient;
std::string makeEndTag(std::string tag) {
	return{"</" + tag.substr(1)};
}

int main(int argc, char** argv) {

	std::string url;
	std::string name = "out.tsv";

	//handle arguments
	std::cout << "CPP web scrapper launched\n";
	if (argc == 1) {
		std::cout << "NO WEBPAGE GIVEN, using http://example.com\n";
		url = "http://example.com";
	}
	else {
		std::cout << "searching \"" << argv[1] << "\"";
		url = argv[1];
		if (argc > 2) {
			for (int x = 0; x < argc; x++) {
				if (argv[x] == "u") {
					name = url;
				}
			}
		}
	}

	std::string HTMLcontent = "";
	std::cout << "sending request\n";
	//setup curl
	CURL* curl;
	CURLcode output;

	curl = curl_easy_init();
	if (curl) {
		curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writeRes);
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, &HTMLcontent);
		curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
		//send curl request 
		output = curl_easy_perform(curl);
		if (output != CURLE_OK) {
			fprintf(stderr, "E: curl_easy_preform() failed: %s\n", curl_easy_strerror(output));
		}
		//gc
		curl_easy_cleanup(curl);
	}
	else {
		std::cout << "E: curl initialization error\n";
		return(1);
	}

	std::cout << "SUCCESS retreiving page contents, formatting for storage\n";

	//all lowercase
	for (char& c : HTMLcontent) {
		c = tolower(c);
	}

	//remove all new line tags
	//remove all new line tags
	while (HTMLcontent.find("\n") != std::string::npos) {
		int index = HTMLcontent.find("\n");
		int length = 1;
		HTMLcontent.erase(index, length);
	}
	

	//remove all tabs (tabs denote next column in .tsv formats)
	while (HTMLcontent.find("\t") != std::string::npos) {
		int index = HTMLcontent.find("\t");
		int length = 1;
		HTMLcontent.erase(index, length);
	}

	
	//removing style and script to make prossessing easier 
	while (HTMLcontent.find("<script") != std::string::npos) {
		int index = HTMLcontent.find("<script");
		int length = HTMLcontent.find("</script>") - index + 9;
		HTMLcontent.erase(index, length);
	}
	while (HTMLcontent.find("<style") != std::string::npos) {
		int index = HTMLcontent.find("<style");
		int length = HTMLcontent.find("</style>") - index + 8;
		HTMLcontent.erase(index, length);
	}

	//remove yahoo finances horrible quote markers
	while (HTMLcontent.find("&quot;") != std::string::npos) {
		int index = HTMLcontent.find("&quot;");
		int length = 6;
		HTMLcontent.erase(index, length);
	}
	std::cout << "format complete, writing to storage\n";

	//make output file 
	std::ofstream out(name.c_str());

	/*****************************************************
	*		   		FORMATTING TSV FILE					 *
	* taglist[] below contains the tags in the order they*
	* appear, feel free to change, add or remove tags    *
	******************************************************/
	std::string tagList[] = {"<title>","<h1>","<h2>","<h3>","<h4>","<h5>","<h6>","<p>" };
	std::vector<std::string> toWrite(sizeof(tagList) / sizeof(tagList[0]), "");

	for (int i = 0; i < sizeof(tagList) / sizeof(tagList[0]); i++) {
		std::string tag = tagList[i];
		std::string endTag = makeEndTag(tag);
		while (HTMLcontent.find(tag) != std::string::npos) {
			int currentIndex = HTMLcontent.find(tag);
			int nextIndex = HTMLcontent.find(endTag);
			if (currentIndex < nextIndex) {
				toWrite.at(i) += HTMLcontent.substr(currentIndex, nextIndex - currentIndex + endTag.length()) + "\t";
				HTMLcontent.erase(currentIndex, nextIndex - currentIndex + endTag.length());
			}
			else {
				break;
			}
		}
		//remove any extra long spaces
		while (toWrite.at(i).find("  ") != std::string::npos) {
			int index = toWrite.at(i).find("  ");
			toWrite.at(i).erase(index, 1);
		}
		//remove and nested tags within target tags
		while (toWrite.at(i).find("<") != std::string::npos) {
			int index = toWrite.at(i).find("<");
			int length = toWrite.at(i).find(">") - index + 1;
			toWrite.at(i).erase(index, length);
		}
	}
	//write queue to file 
	for (int i = 0; i < static_cast<int>(toWrite.size());i++) {
		out << toWrite[i] << "\n";
	}
	std::cout << "finished writting to file\n";
	out.close();

	return(0);
}