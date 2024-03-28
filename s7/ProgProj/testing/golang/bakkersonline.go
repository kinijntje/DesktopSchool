package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"time"

	"github.com/chromedp/cdproto/cdp"
	"github.com/chromedp/chromedp"
)

func main() {
	// Create a new context
	ctx, cancel := chromedp.NewContext(context.Background())
	defer cancel()
	fmt.Print("running")

	// Navigate to the website
	err := chromedp.Run(ctx, chromedp.Navigate("https://webshop.broodenbanketmartens.be/be-nl/martens"))
	if err != nil {
		panic(err)
	}

	// Wait for category links to be present
	var categoryLinks []*cdp.Node
	err = chromedp.Run(ctx, chromedp.Nodes(".list li a.category-link", &categoryLinks, chromedp.ByQueryAll))
	if err != nil {
		panic(err)
	}

	// Extract category URLs
	var categoryURLs []string
	for _, link := range categoryLinks {
		categoryURLs = append(categoryURLs, link.AttributeValue("href"))
	}

	// List to store scraped data
	var allProducts []map[string]interface{}

	// Loop through each category URL and scrape products
	for _, categoryURL := range categoryURLs {
		fmt.Println(categoryURL)
		// Navigate to the category URL
		categoryURL = "https://webshop.broodenbanketmartens.be" + categoryURL
		err := chromedp.Run(ctx, chromedp.Navigate(categoryURL))
		if err != nil {
			fmt.Println("Failed to navigate to category URL:", err)
			continue
		}

		// Wait for product cards to be visible
		var productCards []*cdp.Node
		err = chromedp.Run(ctx,
			chromedp.Nodes(".blocks.product-card", &productCards, chromedp.ByQueryAll),
			chromedp.WaitVisible(".blocks.product-card"),
			chromedp.NodeReady(".blocks.product-card"),
		)

		// Extract and store product names, images, and prices for this category
		var categoryProducts []map[string]interface{}
		for _, card := range productCards {
			fmt.Println(card)
			var product map[string]interface{}

			err := chromedp.Run(ctx,
				chromedp.Sleep(10*time.Second),
				chromedp.WaitVisible(fmt.Sprintf("%s .product-title", card.FullXPath())),
				chromedp.WaitVisible(fmt.Sprintf("%s .cover", card.FullXPath())),
				chromedp.WaitVisible(fmt.Sprintf("%s .price.total", card.FullXPath())),
			)
			fmt.Println("going")
			if err != nil {
				fmt.Println("Failed to wait for product card elements:", err)
				continue
			}

			// Extract product name
			var productName string
			err = chromedp.Run(ctx, chromedp.TextContent(fmt.Sprintf(`%s .product-title strong`, card.FullXPath()), &productName))
			if err != nil {
				fmt.Println("Failed to get product name:", err)
				continue
			}
			fmt.Println(productName)

			// Extract product image URL
			var productImageURL string
			err = chromedp.Run(ctx, chromedp.Evaluate(`window.getComputedStyle(document.querySelector('.cover')).backgroundImage`, &productImageURL))
			if err != nil {
				fmt.Println("Failed to get product image URL:", err)
				productImageURL = ""
			}

			// Extract product price
			var productPrice string
			err = chromedp.Run(ctx, chromedp.TextContent(fmt.Sprintf(`%s .price.total`, card.FullXPath()), &productPrice))
			if err != nil {
				fmt.Println("Failed to get product price:", err)
				continue
			}

			product = map[string]interface{}{
				"Product Name":      productName,
				"Product Image URL": productImageURL,
				"Product Price":     productPrice,
			}

			// Append the product to the category products list
			categoryProducts = append(categoryProducts, product)
		}

		// Add category products to the main list
		allProducts = append(allProducts, map[string]interface{}{categoryURL: categoryProducts})
	}

	// Convert the scraped data to JSON format
	outputJSON, err := json.MarshalIndent(allProducts, "", "    ")
	if err != nil {
		panic(err)
	}

	// Write the JSON data to an output file
	err = ioutil.WriteFile("bakkerOutput.json", outputJSON, 0644)
	if err != nil {
		panic(err)
	}

	fmt.Println("Scraped data has been successfully written to 'bakkerOutput.json'.")
}
